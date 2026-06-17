"""
用户行为审计日志模型
记录已认证 API 请求的元数据，不保存请求体或敏感字段。
"""

import datetime
import uuid

from app.extensions import db


class UserActionLog(db.Model):
    """用户行为审计日志"""

    __tablename__ = "user_action_logs"

    id = db.Column(db.String(36), primary_key=True, comment="日志ID")
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True,
        index=True,
        comment="用户ID",
    )
    username = db.Column(
        db.String(100), nullable=True, index=True, comment="用户名"
    )  # noqa: E501
    name = db.Column(db.String(100), nullable=True, comment="用户姓名")
    role_id = db.Column(
        db.String(36), nullable=True, index=True, comment="角色ID"
    )  # noqa: E501

    action_type = db.Column(
        db.String(100), nullable=False, index=True, comment="行为类型"
    )
    method = db.Column(db.String(10), nullable=False, comment="HTTP方法")
    path = db.Column(
        db.String(255), nullable=False, index=True, comment="请求路径"
    )  # noqa: E501
    endpoint = db.Column(
        db.String(255), nullable=True, comment="Flask endpoint"
    )  # noqa: E501
    status_code = db.Column(
        db.Integer, nullable=False, index=True, comment="响应状态码"
    )
    client_ip = db.Column(
        db.String(64), nullable=True, index=True, comment="客户端IP"
    )  # noqa: E501
    user_agent = db.Column(db.String(512), nullable=True, comment="User-Agent")
    created_at = db.Column(
        db.BigInteger, nullable=False, index=True, comment="创建时间戳"
    )

    user = db.relationship(
        "User", backref=db.backref("action_logs", lazy=True)
    )  # noqa: E501

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = int(datetime.datetime.now().timestamp() * 1000)

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.username,
            "name": self.name,
            "roleId": self.role_id,
            "actionType": self.action_type,
            "method": self.method,
            "path": self.path,
            "endpoint": self.endpoint,
            "statusCode": self.status_code,
            "clientIp": self.client_ip,
            "userAgent": self.user_agent,
            "createdAt": self.created_at,
        }
