"""
用户行为审计API
"""

from flask import g, request
from flask_restx import Namespace, Resource, fields

from app.services.audit_service import audit_service

api = Namespace("audit", description="用户行为审计API")

action_log_model = api.model(
    "UserActionLog",
    {
        "id": fields.String(description="日志ID"),
        "userId": fields.String(description="用户ID"),
        "username": fields.String(description="用户名"),
        "name": fields.String(description="用户姓名"),
        "roleId": fields.String(description="角色ID"),
        "actionType": fields.String(description="行为类型"),
        "method": fields.String(description="HTTP方法"),
        "path": fields.String(description="请求路径"),
        "endpoint": fields.String(description="Flask endpoint"),
        "statusCode": fields.Integer(description="响应状态码"),
        "clientIp": fields.String(description="客户端IP"),
        "userAgent": fields.String(description="User-Agent"),
        "createdAt": fields.Integer(description="创建时间戳"),
    },
)

pagination_model = api.model(
    "AuditPagination",
    {
        "total": fields.Integer(description="总条数"),
        "page": fields.Integer(description="当前页"),
        "pageSize": fields.Integer(description="每页条数"),
    },
)

action_logs_response = api.model(
    "ActionLogsResponse",
    {
        "status": fields.String(description="响应状态"),
        "logs": fields.List(
            fields.Nested(action_log_model), description="行为日志列表"
        ),
        "pagination": fields.Nested(pagination_model, description="分页信息"),
    },
)


@api.route("/action-logs")
class ActionLogs(Resource):
    @api.doc(
        "list_action_logs",
        params={
            "userId": "用户ID",
            "username": "用户名",
            "actionType": "行为类型",
            "page": "页码，默认1",
            "pageSize": "每页条数，默认20，最大100",
        },
    )
    @api.marshal_with(action_logs_response, code=200)
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    def get(self):
        """管理员查询用户行为日志"""
        user = getattr(g, "audit_user", None)
        if not user:
            return {
                "status": "error",
                "logs": [],
                "pagination": {"total": 0, "page": 1, "pageSize": 20},
            }, 401
        if not audit_service.has_admin_permission(user):
            return {
                "status": "error",
                "logs": [],
                "pagination": {"total": 0, "page": 1, "pageSize": 20},
            }, 403

        result = audit_service.list_action_logs(
            user_id=request.args.get("userId"),
            username=request.args.get("username"),
            action_type=request.args.get("actionType"),
            page=request.args.get("page", 1),
            page_size=request.args.get("pageSize", 20),
        )
        return {"status": "success", **result}, 200
