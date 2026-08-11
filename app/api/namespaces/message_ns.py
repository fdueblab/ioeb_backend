"""
消息系统API
提供成果相关消息的发送、查询、回复功能
"""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.service_message_service import (
    ServiceMessageError,
    service_message_service,
)
from app.utils.auth_utils import get_request_user

# 创建命名空间
api = Namespace("messages", description="消息系统API")


# 定义消息模型
message_model = api.model(
    "Message",
    {
        "id": fields.Integer(description="消息ID"),
        "serviceId": fields.String(description="成果ID"),
        "serviceName": fields.String(description="成果名称"),
        "senderId": fields.String(description="发送者ID"),
        "senderName": fields.String(description="发送者名称"),
        "receiverId": fields.String(description="接收者ID"),
        "receiverName": fields.String(description="接收者名称"),
        "messageType": fields.String(description="消息类型：contact_purchase-购买联系/use_service-使用服务/general-普通消息"),
        "content": fields.String(description="消息内容"),
        "isMine": fields.Boolean(description="是否为当前用户发送的消息"),
        "isRead": fields.Boolean(description="是否已读"),
        "createTime": fields.Integer(description="创建时间戳"),
    },
)

# 定义发送消息请求模型
send_message_model = api.model(
    "SendMessage",
    {
        "serviceId": fields.String(required=True, description="成果ID"),
        "content": fields.String(required=True, description="消息内容"),
    },
)

# 定义回复消息请求模型
reply_message_model = api.model(
    "ReplyMessage",
    {
        "content": fields.String(required=True, description="回复内容"),
    },
)

# 定义消息列表响应模型
messages_response = api.model(
    "MessagesResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="总记录数"),
        "messages": fields.List(fields.Nested(message_model), description="消息列表"),
    },
)

# 定义单个消息响应模型
message_response = api.model(
    "MessageResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "data": fields.Nested(message_model, description="消息信息"),
    },
)

# 定义简单响应模型
simple_response = api.model(
    "SimpleResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
    },
)

# 定义错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="响应状态", default="error"),
        "message": fields.String(description="错误信息"),
    },
)


def _require_login_user():
    """验证用户登录"""
    user = get_request_user()
    if not user:
        return None, ({"status": "error", "message": "请先登录"}, 401)
    return user, None


@api.route("/contact-purchase")
class ContactPurchaseMessage(Resource):
    @api.doc("send_contact_purchase_message")
    @api.expect(send_message_model)
    @api.marshal_with(message_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """发送购买联系消息"""
        user, err = _require_login_user()
        if err:
            return err

        data = request.get_json()
        service_id = data.get("serviceId")
        content = data.get("content")

        if not service_id or not content:
            return {"status": "error", "message": "成果ID和消息内容不能为空"}, 400

        try:
            message = service_message_service.send_purchase_contact_message(
                sender_id=user.id,
                receiver_id=None,  # 接收者从成果的创建者获取
                service_id=service_id,
                content=content,
            )
            return {"status": "success", "message": "消息发送成功", "data": message}, 201
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/use-service")
class UseServiceMessage(Resource):
    @api.doc("send_use_service_message")
    @api.expect(send_message_model)
    @api.marshal_with(message_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """发送使用服务消息"""
        user, err = _require_login_user()
        if err:
            return err

        data = request.get_json()
        service_id = data.get("serviceId")
        content = data.get("content")

        if not service_id or not content:
            return {"status": "error", "message": "成果ID和消息内容不能为空"}, 400

        try:
            message = service_message_service.send_use_service_message(
                sender_id=user.id,
                receiver_id=None,  # 接收者从成果的创建者获取
                service_id=service_id,
                content=content,
            )
            return {"status": "success", "message": "消息发送成功", "data": message}, 201
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/service/<string:service_id>")
class ServiceMessageList(Resource):
    @api.doc("get_service_messages")
    @api.marshal_with(messages_response, code=200)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def get(self, service_id):
        """获取成果的消息列表"""
        user, err = _require_login_user()
        if err:
            return err

        try:
            messages = service_message_service.get_service_messages(service_id, user.id)
            return {
                "status": "success",
                "message": "获取消息列表成功",
                "total": len(messages),
                "messages": messages,
            }, 200
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/<int:message_id>/reply")
class MessageReply(Resource):
    @api.doc("reply_message")
    @api.expect(reply_message_model)
    @api.marshal_with(message_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(401, "Unauthorized", error_response)
    @api.response(404, "Message not found", error_response)
    @api.response(500, "Server error", error_response)
    def post(self, message_id):
        """回复消息"""
        user, err = _require_login_user()
        if err:
            return err

        data = request.get_json()
        content = data.get("content")

        if not content:
            return {"status": "error", "message": "回复内容不能为空"}, 400

        try:
            message = service_message_service.reply_message(message_id, user.id, content)
            return {"status": "success", "message": "回复成功", "data": message}, 201
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/user/unread")
class UserUnreadMessages(Resource):
    @api.doc("get_user_unread_messages")
    @api.marshal_with(messages_response, code=200)
    @api.response(401, "Unauthorized", error_response)
    @api.response(500, "Server error", error_response)
    def get(self):
        """获取用户未读消息列表"""
        user, err = _require_login_user()
        if err:
            return err

        try:
            messages = service_message_service.get_user_unread_messages(user.id)
            return {
                "status": "success",
                "message": "获取未读消息成功",
                "total": len(messages),
                "messages": messages,
            }, 200
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/<int:message_id>/mark-read")
class MessageMarkRead(Resource):
    @api.doc("mark_message_as_read")
    @api.marshal_with(simple_response, code=200)
    @api.response(401, "Unauthorized", error_response)
    @api.response(404, "Message not found", error_response)
    @api.response(500, "Server error", error_response)
    def post(self, message_id):
        """标记消息为已读"""
        user, err = _require_login_user()
        if err:
            return err

        try:
            service_message_service.mark_message_as_read(message_id, user.id)
            return {"status": "success", "message": "标记成功"}, 200
        except ServiceMessageError as e:
            return {"status": "error", "message": str(e)}, 500