"""
用户行为审计服务
提供认证用户解析、请求自动记录和管理员查询能力。
"""

import datetime
from typing import Optional

from flask import current_app, g, request
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.user.role_permission import RolePermission
from app.models.user.user import User
from app.models.user.user_tokens import UserToken
from app.models.user_action_log import UserActionLog


class AuditService:
    """审计日志服务"""

    SKIP_PATH_PREFIXES = (
        "/api/docs",
        "/api/swagger",
        "/swagger",
        "/static",
    )
    SKIP_PATHS = {
        "/api/health",
        "/api/audit/action-logs",
    }

    def __init__(self):
        self._table_checked = False

    def ensure_table(self):
        """在没有迁移目录的部署环境中按需创建审计表。"""
        if self._table_checked:
            return
        try:
            UserActionLog.__table__.create(db.engine, checkfirst=True)
            self._table_checked = True
        except SQLAlchemyError as exc:
            db.session.rollback()
            current_app.logger.warning("审计日志表检查/创建失败: %s", exc)

    def get_user_from_token(self, token: str) -> Optional[User]:
        if not token:
            return None

        user_token = UserToken.query.filter_by(token=token).first()
        if not user_token:
            return None

        now = int(datetime.datetime.now().timestamp() * 1000)
        if user_token.expires_at < now:
            return None

        user = User.query.filter_by(id=user_token.user_id, deleted=0).first()
        if not user or user.status != 1:
            return None

        return user

    def attach_request_user(self):
        """在请求进入业务处理前解析用户，避免登出时 token 被删除后丢失用户信息。"""
        token = request.headers.get("Access-Token", "")
        g.audit_user = self.get_user_from_token(token)

    def has_admin_permission(self, user: Optional[User]) -> bool:
        if not user:
            return False
        if user.role_id in ("admin", "root"):
            return True
        return (
            RolePermission.query.filter_by(
                role_id=user.role_id,
                permission_id="admin",
            ).first()
            is not None
        )

    def should_log_request(self) -> bool:
        if request.method == "OPTIONS":
            return False
        path = request.path or ""
        if path in self.SKIP_PATHS:
            return False
        return path.startswith("/api/") and not any(
            path.startswith(prefix) for prefix in self.SKIP_PATH_PREFIXES
        )

    def infer_action_type(self) -> str:
        method = request.method.upper()
        path = request.path or ""

        if path == "/api/auth/login" and method == "POST":
            return "auth.login"
        if path == "/api/auth/logout" and method == "POST":
            return "auth.logout"
        if path == "/api/auth/info" and method == "GET":
            return "auth.info"
        if path == "/api/auth/register" and method == "POST":
            return "auth.register"

        if path == "/api/users":
            return "users.create" if method == "POST" else "users.list"
        if path.startswith("/api/users/"):
            if path.endswith("/update"):
                return "users.update"
            if path.endswith("/delete"):
                return "users.delete"
            if path.endswith("/status"):
                return "users.status"
            if path.endswith("/password"):
                return "users.password"
            if path.endswith("/role"):
                return "users.role"
            return "users.detail"

        if path.startswith("/api/services/"):
            if path.endswith("/deploy"):
                return "services.deploy"
            if path.endswith("/stop"):
                return "services.stop"
            if path.endswith("/delete"):
                return "services.delete"
            if path.endswith("/publish"):
                return "services.publish"
            return "services.request"

        if path.startswith("/api/datasets"):
            return "datasets.request"
        if path.startswith("/api/dictionaries"):
            return "dictionaries.request"
        if path.startswith("/api/audit"):
            return "audit.request"
        return "api.request"

    def get_client_ip(self) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.headers.get("X-Real-IP") or request.remote_addr or ""

    def log_request(self, response):
        if not self.should_log_request():
            return response

        user = getattr(g, "audit_user", None)
        if not user:
            return response

        self.log_action(
            user=user,
            action_type=self.infer_action_type(),
            method=request.method,
            path=request.path,
            endpoint=request.endpoint,
            status_code=response.status_code,
            client_ip=self.get_client_ip(),
            user_agent=(request.headers.get("User-Agent") or "")[:512],
        )
        return response

    def log_action(
        self,
        user: User,
        action_type: str,
        method: str,
        path: str,
        endpoint: str,
        status_code: int,
        client_ip: str,
        user_agent: str,
    ):
        try:
            self.ensure_table()
            log = UserActionLog(
                user_id=user.id,
                username=user.username,
                name=user.name,
                role_id=user.role_id,
                action_type=action_type,
                method=method.upper(),
                path=path[:255],
                endpoint=(endpoint or "")[:255],
                status_code=status_code,
                client_ip=(client_ip or "")[:64],
                user_agent=(user_agent or "")[:512],
            )
            db.session.add(log)
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            current_app.logger.warning("记录用户行为日志失败: %s", exc)

    def list_action_logs(
        self,
        user_id: str = None,
        username: str = None,
        action_type: str = None,
        page: int = 1,
        page_size: int = 20,
    ):
        self.ensure_table()
        page = max(int(page or 1), 1)
        page_size = min(max(int(page_size or 20), 1), 100)

        query = UserActionLog.query
        if user_id:
            query = query.filter(UserActionLog.user_id == user_id)
        if username:
            query = query.filter(UserActionLog.username == username)
        if action_type:
            query = query.filter(UserActionLog.action_type == action_type)

        total = query.count()
        logs = (
            query.order_by(UserActionLog.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "logs": [log.to_dict() for log in logs],
            "pagination": {
                "total": total,
                "page": page,
                "pageSize": page_size,
            },
        }


audit_service = AuditService()
