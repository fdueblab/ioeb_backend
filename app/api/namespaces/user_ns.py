from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.user_service import UserServiceError, user_service

# 创建命名空间
api = Namespace("users", description="用户管理API")

# 定义模型
user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True, description="用户ID"),
        "username": fields.String(required=True, description="用户名"),
        "name": fields.String(required=True, description="用户姓名"),
        "avatar": fields.String(description="头像路径"),
        "telephone": fields.String(description="电话号码"),
        "merchantCode": fields.String(description="商户代码"),
        "roleId": fields.String(description="角色ID"),
        "status": fields.Integer(description="用户状态"),
        "deleted": fields.Integer(description="是否删除"),
        "lastLoginIp": fields.String(description="最后登录IP"),
        "lastLoginTime": fields.Integer(description="最后登录时间戳"),
        "createTime": fields.Integer(description="创建时间戳"),
        "creatorId": fields.String(description="创建者ID"),
    },
)

user_post_model = api.model(
    "UserCreate",
    {
        "username": fields.String(required=True, description="用户名"),
        "name": fields.String(required=True, description="用户姓名"),
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

        if not data or not data.get("username") or not data.get("name"):
            api.abort(400, "缺少必要的用户信息")

        try:
            user_data, is_new = user_service.create_user(data.get("username"), data.get("name"))

            if not is_new:
                return {"status": "warning", "message": "用户已存在", "user": user_data}, 200

            return {"status": "success", "message": "用户创建成功", "user": user_data}, 201
        except UserServiceError as e:
            api.abort(400, str(e))


@api.route("/<string:id>")
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
