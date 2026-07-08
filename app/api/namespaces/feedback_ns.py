"""
意见反馈 API
提供用户反馈提交和管理员查看能力。
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.feedback import Feedback
from app.models.user.role_permission import RolePermission
from app.utils.auth_utils import get_request_user

SUCCESS_SUBMIT_MESSAGE = "感谢您的意见，我们将进行论证！"

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
        "displayStatus": fields.String(description="用户可见状态"),
        "responseSummary": fields.String(description="平台处理总结"),
        "respondedAt": fields.Integer(description="平台回复时间"),
        "feishuStatus": fields.String(description="飞书处理状态"),
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


def has_admin_permission(user):
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


@api.route("")
class FeedbackList(Resource):
    @api.doc("create_feedback")
    @api.expect(feedback_create_model)
    @api.marshal_with(feedback_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """提交意见反馈（需登录）"""
        user = get_request_user()
        if not user:
            return {"status": "error", "message": "请先登录后再提交反馈"}, 401

        data = request.get_json(silent=True) or {}
        content = str(data.get("content") or "").strip()

        if not content:
            return {"status": "error", "message": "反馈内容不能为空"}, 400

        title = content[:30] or "用户意见反馈"
        feedback = Feedback(
            user_id=user.id,
            username=user.username or user.name or "用户",
            feedback_type="意见反馈",
            title=title[:100],
            content=content[:2000],
            feishu_status="待处理",
        )

        try:
            db.session.add(feedback)
            db.session.commit()
            return {
                "status": "success",
                "message": SUCCESS_SUBMIT_MESSAGE,
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
        user = get_request_user()
        if not has_admin_permission(user):
            return {"status": "error", "message": "无权限查看反馈列表"}, 403

        try:
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


@api.route("/mine")
class MyFeedbackList(Resource):
    @api.doc("list_my_feedbacks")
    @api.marshal_with(feedback_list_response, code=200)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def get(self):
        """当前登录用户查看自己的反馈记录"""
        user = get_request_user()
        if not user:
            return {"status": "error", "message": "请先登录后再查看反馈记录"}, 401

        try:
            feedbacks = (
                Feedback.query.filter_by(user_id=user.id)
                .order_by(Feedback.created_at.desc())
                .all()
            )
            return {
                "status": "success",
                "message": "获取反馈记录成功",
                "total": len(feedbacks),
                "feedbacks": [item.to_dict() for item in feedbacks],
            }, 200
        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"status": "error", "message": f"反馈查询失败: {str(exc)}"}, 500
