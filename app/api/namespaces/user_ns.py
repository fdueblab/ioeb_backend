from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.user_service import UserServiceError, user_service

# 创建命名空间
api = Namespace("users", description="用户管理API")

# 定义模型
user_model = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="用户ID"),
        "username": fields.String(required=True, description="用户名"),
        "email": fields.String(required=True, description="电子邮箱"),
        "created_at": fields.DateTime(readonly=True, description="创建时间"),
        "updated_at": fields.DateTime(readonly=True, description="更新时间"),
    },
)

user_post_model = api.model(
    "UserCreate",
    {
        "username": fields.String(required=True, description="用户名"),
        "email": fields.String(required=True, description="电子邮箱"),
    },
)

user_response = api.model(
    "UserResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "user": fields.Nested(user_model, description="用户信息"),
    },
)

users_response = api.model(
    "UsersResponse",
    {
        "status": fields.String(description="响应状态"),
        "users": fields.List(fields.Nested(user_model), description="用户列表"),
    },
)


@api.route("")
class UserList(Resource):
    @api.doc("list_users")
    @api.marshal_with(users_response, code=200)
    def get(self):
        """获取所有用户"""
        users = user_service.get_all_users()
        return {"status": "success", "users": users}, 200

    @api.doc("create_user")
    @api.expect(user_post_model)
    @api.marshal_with(user_response, code=201)
    @api.response(400, "Invalid input")
    @api.response(409, "User already exists")
    def post(self):
        """创建新用户"""
        data = request.get_json()

        if not data or not data.get("username") or not data.get("email"):
            api.abort(400, "缺少必要的用户信息")

        try:
            user_data, is_new = user_service.create_user(data.get("username"), data.get("email"))

            if not is_new:
                return {"status": "warning", "message": "用户已存在", "user": user_data}, 200

            return {"status": "success", "message": "用户创建成功", "user": user_data}, 201
        except UserServiceError as e:
            api.abort(400, str(e))


@api.route("/<int:id>")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserResource(Resource):
    @api.doc("get_user")
    @api.marshal_with(user_response)
    def get(self, id):
        """获取指定ID的用户"""
        try:
            user = user_service.get_user_by_id(id)
            return {"status": "success", "message": "获取用户成功", "user": user}
        except UserServiceError as e:
            api.abort(404, str(e))
