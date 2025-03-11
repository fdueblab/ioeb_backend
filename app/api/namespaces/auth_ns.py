"""
认证相关API
提供登录、登出等认证功能
"""

import datetime
import secrets

from flask import request
from flask_restx import Namespace, Resource, fields

from app.extensions import db
from app.models.user.role import Role
from app.models.user.role_permission import RolePermission
from app.models.user.user import User
from app.models.user.user_tokens import UserToken

# 创建命名空间
api = Namespace("auth", description="认证相关API")

# 定义请求模型
login_model = api.model(
    "Login",
    {
        "username": fields.String(required=True, description="用户名"),
        "password": fields.String(required=True, description="密码"),
    },
)

# 添加权限模型
permission_model = api.model(
    "Permission",
    {
        "roleId": fields.String(description="角色ID"),
        "permissionId": fields.String(description="权限ID"),
        "permissionName": fields.String(description="权限名称"),
        "dataAccess": fields.Raw(description="数据访问权限"),
    },
)

# 定义角色模型
role_model = api.model(
    "Role",
    {
        "id": fields.String(description="角色ID"),
        "name": fields.String(description="角色名称"),
        "describe": fields.String(description="角色描述"),
        "status": fields.Integer(description="状态"),
        "creatorId": fields.String(description="创建者ID"),
        "createTime": fields.Integer(description="创建时间"),
        "deleted": fields.Integer(description="是否删除"),
        # 以下两个字段在login的response中无要求，但在info的response中要求
        # 为了保持response的一致性，在login的response中也添加这两个字段
        "permissions": fields.List(fields.Nested(permission_model), description="权限详情"),
        "permissionList": fields.List(fields.String, description="权限ID列表"),
    },
)

# 定义用户响应模型
user_response = api.model(
    "UserResponse",
    {
        "id": fields.String(description="用户ID"),
        "name": fields.String(description="用户姓名"),
        "username": fields.String(description="用户名"),
        "password": fields.String(description="密码", default=""),
        "token": fields.String(description="令牌"),
        "avatar": fields.String(description="头像"),
        "status": fields.Integer(description="状态"),
        "telephone": fields.String(description="电话号码"),
        "lastLoginIp": fields.String(description="最后登录IP"),
        "lastLoginTime": fields.Integer(description="最后登录时间"),
        "creatorId": fields.String(description="创建者ID"),
        "createTime": fields.Integer(description="创建时间"),
        "merchantCode": fields.String(description="商户代码"),
        "deleted": fields.Integer(description="是否删除"),
        "roleId": fields.String(description="角色ID"),
        "role": fields.Nested(role_model, description="角色信息"),
    },
)

# 定义标准响应模型
standard_response = api.model(
    "StandardResponse",
    {
        "message": fields.String(description="响应消息"),
        "timestamp": fields.Integer(description="时间戳"),
        "result": fields.Nested(user_response, description="响应结果"),
        "code": fields.Integer(description="响应代码"),
    },
)

# 错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "code": fields.Integer(description="错误码"),
        "message": fields.String(description="错误信息"),
    },
)


@api.route("/login")
class Login(Resource):
    @api.doc(
        "user_login",
        responses={
            200: ("登录成功", user_response),
            400: ("参数错误", error_response),
            401: ("认证失败", error_response),
            500: ("服务器错误", error_response),
        },
    )
    @api.expect(login_model)
    def post(self):
        """用户登录"""
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # 参数验证
        if not username or not password:
            return {"code": 400, "message": "用户名和密码不能为空"}, 400

        # 查询用户
        user = User.query.filter_by(username=username, deleted=0).first()

        # 验证用户存在并检查密码
        if not user or user.password != password:  # 实际应用中应该使用安全的密码比对方法
            return {"code": 401, "message": "用户名或密码错误"}, 401

        # 检查用户状态
        if user.status != 1:
            return {"code": 401, "message": "账户已禁用"}, 401

        # 生成令牌
        token = secrets.token_hex(16)

        # 更新用户登录信息
        user.last_login_ip = request.remote_addr
        user.last_login_time = int(datetime.datetime.now().timestamp())

        # 查询用户角色
        role = Role.query.filter_by(id=user.role_id, deleted=0).first()

        # 创建或更新令牌
        expires_at = int(datetime.datetime.now().timestamp()) + 7 * 24 * 60 * 60  # 7天过期
        user_token = UserToken.query.filter_by(user_id=user.id).first()

        if user_token:
            user_token.token = token
            user_token.expires_at = expires_at
        else:
            user_token = UserToken(user_id=user.id, token=token, expires_at=expires_at)
            db.session.add(user_token)

        db.session.commit()

        # 构建响应
        response = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "password": "",  # 不返回密码
            "token": token,
            "avatar": user.avatar or "",
            "status": user.status,
            "telephone": user.telephone or "",
            "lastLoginIp": user.last_login_ip or "",
            "lastLoginTime": user.last_login_time or 0,
            "creatorId": user.creator_id or "",
            "createTime": user.create_time,
            "merchantCode": user.merchant_code or "",
            "deleted": user.deleted,
            "roleId": user.role_id or "",
            "role": role.to_dict() if role else None,
        }

        return response, 200


@api.route("/info")
class UserInfo(Resource):
    @api.doc(
        "get_user_info",
        responses={
            200: ("获取用户信息成功", user_response),
            401: ("认证失败", error_response),
            500: ("服务器错误", error_response),
        },
    )
    def get(self):
        """获取用户信息"""
        token = request.headers.get("Access-Token", "")

        if not token:
            return {"code": 401, "message": "未提供认证令牌"}, 401

        # 查询令牌
        user_token = UserToken.query.filter_by(token=token).first()

        if not user_token:
            return {"code": 401, "message": "无效的认证令牌"}, 401

        # 检查令牌是否过期
        now = int(datetime.datetime.now().timestamp())
        if user_token.expires_at < now:
            return {"code": 401, "message": "认证令牌已过期"}, 401

        # 查询用户
        user = User.query.filter_by(id=user_token.user_id, deleted=0).first()

        if not user:
            return {"code": 401, "message": "用户不存在或已删除"}, 401

        # 检查用户状态
        if user.status != 1:
            return {"code": 401, "message": "账户已禁用"}, 401

        # 查询用户角色
        role = Role.query.filter_by(id=user.role_id, deleted=0).first()

        # 获取权限信息
        role_permissions = RolePermission.query.filter(RolePermission.role_id == role.id).all()

        if role:
            role_dict = role.to_dict()
            # 这里需要根据你的实际模型结构来获取权限信息
            role_dict["permissions"] = [
                p.to_dict() for p in role_permissions
            ]  # 从数据库获取权限信息
            role_dict["permissionList"] = [
                p.permission_id for p in role_permissions
            ]  # 从数据库获取权限ID列表

        # 构建响应
        user_data = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "password": "",  # 不返回密码
            "token": token,
            "avatar": user.avatar or "",
            "status": user.status,
            "telephone": user.telephone or "",
            "lastLoginIp": user.last_login_ip or "",
            "lastLoginTime": user.last_login_time or 0,
            "creatorId": user.creator_id or "",
            "createTime": user.create_time,
            "merchantCode": user.merchant_code or "",
            "deleted": user.deleted,
            "roleId": user.role_id or "",
            "role": role_dict if role_dict else None,
        }

        response = {
            "message": "",
            "timestamp": int(datetime.datetime.now().timestamp() * 1000),  # 转换为毫秒
            "result": user_data,
            "code": 200,
        }

        return response, 200


@api.route("/logout")
class Logout(Resource):
    @api.doc(
        "user_logout",
        responses={
            200: "登出成功",
            401: ("认证失败", error_response),
        },
    )
    def post(self):
        """用户登出"""
        token = request.headers.get("Access-Token", "")

        if token:
            # 查询并删除令牌
            user_token = UserToken.query.filter_by(token=token).first()
            if user_token:
                db.session.delete(user_token)
                db.session.commit()

        return {"message": "登出成功"}, 200
