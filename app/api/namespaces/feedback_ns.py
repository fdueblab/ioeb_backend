"""
意见反馈 API
提供用户反馈提交和管理员查看能力。
"""

from flask import g, request
from flask_restx import Namespace, Resource, fields
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.feedback import Feedback
from app.services.audit_service import audit_service


api = Namespace("feedback", description="意见反馈API")

feedback_model = api.model(
    "Feedback",
    {
        "id": fields.String(description="反馈ID"),
        "userId": fields.String(description="用户ID"),
        "username": fields.String(description="用户名"),
        "feedbackType": fields.String(description="反馈类型"),
        "title": fields.String(description="反馈标题"),
        "content": fields.String(description="反馈内容"),
        "contact": fields.String(description="联系方式"),
        "status": fields.String(description="状态"),
        "feishuRecordId": fields.String(description="飞书多维表格记录ID"),
        "feishuSyncStatus": fields.String(description="飞书同步状态"),
        "feishuSyncError": fields.String(description="飞书同步错误"),
        "feishuSyncedAt": fields.Integer(description="飞书同步时间"),
        "createdAt": fields.Integer(description="创建时间"),
    },
)

feedback_create_model = api.model(
    "FeedbackCreate",
    {
        "content": fields.String(required=True, description="反馈内容"),
    },
)

feedback_response = api.model(
    "FeedbackResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "feedback": fields.Nested(feedback_model, description="反馈信息"),
    },
)

feedback_list_response = api.model(
    "FeedbackListResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="总数"),
        "feedbacks": fields.List(fields.Nested(feedback_model), description="反馈列表"),
    },
)

error_response = api.model(
    "FeedbackErrorResponse",
    {
        "status": fields.String(description="响应状态", default="error"),
        "message": fields.String(description="错误信息"),
    },
)


def ensure_feedback_table():
    table_name = Feedback.__tablename__
    Feedback.__table__.create(db.engine, checkfirst=True)
    inspector = inspect(db.engine)
    if table_name not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    missing_columns = {
        "feishu_record_id": "VARCHAR(100)",
        "feishu_sync_status": "VARCHAR(20)",
        "feishu_sync_error": "TEXT",
        "feishu_synced_at": "BIGINT",
    }
    for column_name, column_type in missing_columns.items():
        if column_name not in existing_columns:
            db.session.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            )
    db.session.commit()


@api.route("")
class FeedbackList(Resource):
    @api.doc("create_feedback")
    @api.expect(feedback_create_model)
    @api.marshal_with(feedback_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """提交意见反馈"""
        data = request.get_json(silent=True) or {}
        content = str(data.get("content") or "").strip()

        if not content:
            return {"status": "error", "message": "反馈内容不能为空"}, 400

        user = getattr(g, "audit_user", None)
        title = content[:30] or "用户意见反馈"
        feedback = Feedback(
            user_id=user.id if user else None,
            username=(user.username if user else None) or "匿名用户",
            feedback_type="意见反馈",
            title=title[:100],
            content=content[:2000],
        )

        try:
            ensure_feedback_table()
            db.session.add(feedback)
            db.session.commit()
            return {
                "status": "success",
                "message": "反馈提交成功",
                "feedback": feedback.to_dict(),
            }, 201
        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"status": "error", "message": f"反馈保存失败: {str(exc)}"}, 500

    @api.doc("list_feedbacks")
    @api.marshal_with(feedback_list_response, code=200)
    @api.response(403, "Forbidden", error_response)
    @api.response(500, "Server error", error_response)
    def get(self):
        """管理员查看反馈列表"""
        user = getattr(g, "audit_user", None)
        if not audit_service.has_admin_permission(user):
            return {"status": "error", "message": "无权限查看反馈列表"}, 403

        try:
            ensure_feedback_table()
            feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
            return {
                "status": "success",
                "message": "获取反馈列表成功",
                "total": len(feedbacks),
                "feedbacks": [item.to_dict() for item in feedbacks],
            }, 200
        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"status": "error", "message": f"反馈查询失败: {str(exc)}"}, 500
