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
        "password": fields.String(required=True, description="用户密码"),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "username": fields.String(description="用户名"),
        "name": fields.String(description="用户姓名"),
        "avatar": fields.String(description="头像路径"),
        "telephone": fields.String(description="电话号码"),
        "merchantCode": fields.String(description="商户代码"),
    },
)

user_password_model = api.model(
    "UserPasswordUpdate",
    {
        "password": fields.String(required=True, description="新密码"),
    },
)

user_role_model = api.model(
    "UserRoleUpdate",
    {
        "roleId": fields.String(required=True, description="角色ID"),
    },
)

user_status_model = api.model(
    "UserStatus",
    {
        "status": fields.Integer(required=True, description="用户状态：1-正常，0-禁用"),
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

simple_response = api.model(
    "SimpleResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
    },
)


@api.route("")
class UserList(Resource):
    @api.doc("list_users")
    @api.marshal_with(users_response, code=200)
    def get(self):
        """获取所有用户（不包含已删除的用户）"""
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

        if not data or not data.get("username") or not data.get("name") or not data.get("password"):
            api.abort(400, "缺少必要的用户信息")

        try:
            user_data, is_new = user_service.create_user(
                data.get("username"), 
                data.get("name"), 
                data.get("password")
            )

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
        """获取指定ID的用户（已删除的用户会返回"用户已删除"错误）"""
        try:
            user = user_service.get_user_by_id(id)
            return {"status": "success", "message": "获取用户成功", "user": user}
        except UserServiceError as e:
            api.abort(404, str(e))


@api.route("/<string:id>/update")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserUpdateResource(Resource):
    @api.doc("update_user")
    @api.expect(user_update_model)
    @api.marshal_with(user_response, code=200)
    @api.response(400, "Invalid input")
    @api.response(404, "User not found")
    def post(self, id):
        """更新用户信息（已删除的用户会返回"用户已删除"错误）"""
        data = request.get_json()

        if not data:
            api.abort(400, "缺少必要的用户信息")

        try:
            user = user_service.update_user(id, data)
            return {"status": "success", "message": "用户信息更新成功", "user": user}
        except UserServiceError as e:
            api.abort(404, str(e))


@api.route("/<string:id>/delete")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserDeleteResource(Resource):
    @api.doc("delete_user")
    @api.marshal_with(simple_response, code=200)
    @api.response(404, "User not found")
    def get(self, id):
        """删除用户（已删除的用户会返回"用户已删除"错误）"""
        try:
            user_service.delete_user(id)
            return {"status": "success", "message": "用户删除成功"}
        except UserServiceError as e:
            api.abort(404, str(e))


@api.route("/<string:id>/status")
@api.param("id", "用户ID")
@api.param("status", "用户状态：1-正常，0-禁用")
@api.response(404, "User not found")
class UserStatusResource(Resource):
    @api.doc("update_user_status")
    @api.marshal_with(simple_response, code=200)
    @api.response(400, "Invalid input")
    @api.response(404, "User not found")
    def get(self, id):
        """更新用户状态（已删除的用户会返回"用户已删除"错误）"""
        status = request.args.get("status")
        
        if not status:
            api.abort(400, "缺少必要的用户状态参数")

        try:
            status_int = int(status)
            if status_int not in [0, 1]:
                api.abort(400, "用户状态值无效，只能是0（禁用）或1（正常）")
            
            user_service.update_user_status(id, status_int)
            return {"status": "success", "message": "用户状态更新成功"}
        except ValueError:
            api.abort(400, "状态参数必须是数字")
        except UserServiceError as e:
            api.abort(404, str(e))


@api.route("/<string:id>/password")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserPasswordResource(Resource):
    @api.doc("update_user_password")
    @api.expect(user_password_model)
    @api.marshal_with(simple_response, code=200)
    @api.response(400, "Invalid input")
    @api.response(404, "User not found")
    def post(self, id):
        """更新用户密码（已删除的用户会返回"用户已删除"错误）"""
        data = request.get_json()

        if not data or not data.get("password"):
            api.abort(400, "缺少必要的密码信息")

        try:
            user_service.update_user_password(id, data.get("password"))
            return {"status": "success", "message": "用户密码更新成功"}
        except UserServiceError as e:
            api.abort(404, str(e))


@api.route("/<string:id>/role")
@api.param("id", "用户ID")
@api.response(404, "User not found")
class UserRoleResource(Resource):
    @api.doc("update_user_role")
    @api.expect(user_role_model)
    @api.marshal_with(simple_response, code=200)
    @api.response(400, "Invalid input")
    @api.response(404, "User not found")
    def post(self, id):
        """更新用户角色（已删除的用户会返回"用户已删除"错误）"""
        data = request.get_json()

        if not data or not data.get("roleId"):
            api.abort(400, "缺少必要的角色信息")

        try:
            user_service.update_user_role(id, data.get("roleId"))
            return {"status": "success", "message": "用户角色更新成功"}
        except UserServiceError as e:
            api.abort(404, str(e))
