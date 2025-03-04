from flask import request
from flask_restx import Namespace, Resource, fields

from app.extensions import db
from app.models import User

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
        users = User.query.all()
        return {"status": "success", "users": [user.to_dict() for user in users]}, 200

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

        # 检查用户是否已存在
        if User.query.filter_by(email=data.get("email")).first():
            api.abort(409, "用户已存在")

        new_user = User(username=data.get("username"), email=data.get("email"))

        db.session.add(new_user)
        db.session.commit()

        return {"status": "success", "message": "用户创建成功", "user": new_user.to_dict()}, 201


@api.route("/<int:id>")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserResource(Resource):
    @api.doc("get_user")
    @api.marshal_with(user_response)
    def get(self, id):
        """获取指定ID的用户"""
        user = User.query.get(id)
        if not user:
            api.abort(404, f"用户ID {id} 不存在")

        return {"status": "success", "message": "获取用户成功", "user": user.to_dict()}
