"""
认证相关API
提供登录、登出、微信小程序登录等认证功能
"""

import datetime
import secrets
import uuid

import requests as http_requests
from flask import request, current_app
from flask_restx import Namespace, Resource, fields

from app.extensions import db
from app.models.user.role import Role
from app.models.user.role_permission import RolePermission
from app.models.user.user import User
from app.models.user.user_tokens import UserToken
from app.utils.password_utils import verify_password, hash_password

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
        "timestamp": fields.Integer(description="时间戳（毫秒）"),
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

# 角色列表响应模型
roles_response = api.model(
    "RolesResponse",
    {
        "status": fields.String(description="响应状态"),
        "roles": fields.List(fields.Nested(role_model), description="角色列表"),
    },
)


# 微信登录请求模型
wx_login_model = api.model(
    "WxLogin",
    {
        "code": fields.String(required=True, description="wx.login 返回的 code"),
        "nickName": fields.String(description="微信昵称（可选）"),
        "avatarUrl": fields.String(description="微信头像 URL（可选）"),
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
        if not user or not verify_password(password, user.password):
            return {"code": 401, "message": "用户名或密码错误"}, 401

        # 检查用户状态
        if user.status != 1:
            return {"code": 401, "message": "账户已禁用"}, 401

        # 生成令牌
        token = secrets.token_hex(16)

        # 更新用户登录信息
        user.last_login_ip = request.remote_addr
        user.last_login_time = int(datetime.datetime.now().timestamp() * 1000) # 毫秒时间戳

        # 查询用户角色
        role = Role.query.filter_by(id=user.role_id, deleted=0).first()

        # 创建或更新令牌
        expires_at = int(datetime.datetime.now().timestamp() * 1000) + 7 * 24 * 60 * 60 * 1000 # 7天过期
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
        now = int(datetime.datetime.now().timestamp() * 1000) # 毫秒时间戳
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


@api.route("/roles")
class Roles(Resource):
    @api.doc(
        "get_all_roles",
        responses={
            200: ("获取角色列表成功", roles_response),
            500: ("服务器错误", error_response),
        },
    )
    @api.marshal_with(roles_response, code=200)
    def get(self):
        """获取所有角色（不包含已删除的角色）"""
        try:
            # 查询所有未删除的角色
            roles = Role.query.filter_by(deleted=0).all()
            roles_data = [role.to_dict() for role in roles]
            
            return {"status": "success", "roles": roles_data}, 200
        except Exception as e:
            return {"status": "error", "message": f"获取角色列表失败: {str(e)}"}, 500


@api.route("/wx_login")
class WxLogin(Resource):
    @api.doc(
        "wx_login",
        responses={
            200: ("微信登录成功", user_response),
            400: ("参数错误", error_response),
            401: ("微信认证失败", error_response),
            500: ("服务器错误", error_response),
        },
    )
    @api.expect(wx_login_model)
    def post(self):
        """微信小程序登录（code 换 openid，自动注册/登录）"""
        data = request.json
        code = data.get("code")
        nick_name = data.get("nickName", "")
        avatar_url = data.get("avatarUrl", "")

        if not code:
            return {"code": 400, "message": "缺少 code 参数"}, 400

        # 用 code 向微信服务器换取 openid
        app_id = current_app.config.get("WX_APP_ID", "")
        app_secret = current_app.config.get("WX_APP_SECRET", "")

        if not app_secret:
            current_app.logger.warning("WX_APP_SECRET 未配置，使用固定开发 openid（仅开发环境）")
            openid = f"dev_{app_id}"
        else:
            try:
                wx_url = (
                    "https://api.weixin.qq.com/sns/jscode2session"
                    f"?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
                )
                wx_resp = http_requests.get(wx_url, timeout=10)
                wx_data = wx_resp.json()

                if "openid" not in wx_data:
                    err_msg = wx_data.get("errmsg", "微信接口返回异常")
                    current_app.logger.error(f"微信 jscode2session 失败: {wx_data}")
                    return {"code": 401, "message": f"微信认证失败: {err_msg}"}, 401

                openid = wx_data["openid"]
            except Exception as e:
                current_app.logger.error(f"请求微信接口异常: {e}")
                return {"code": 500, "message": "请求微信服务器失败"}, 500

        # 按 openid 查找已有用户
        user = User.query.filter_by(wx_openid=openid, deleted=0).first()

        if not user:
            # 自动创建新用户
            user_id = str(uuid.uuid4())
            now_ms = int(datetime.datetime.now().timestamp() * 1000)
            user = User(
                id=user_id,
                username=f"wx_{openid[:16]}",
                name=nick_name or f"微信用户",
                password=hash_password(secrets.token_hex(16)),
                avatar=avatar_url or "",
                wx_openid=openid,
                role_id="user",
                status=1,
                deleted=0,
                create_time=now_ms,
            )
            db.session.add(user)
            current_app.logger.info(f"微信登录自动创建用户: {user.username} (openid={openid[:8]}...)")
        else:
            # 更新昵称和头像（如果用户传了新的）
            if nick_name:
                user.name = nick_name
            if avatar_url:
                user.avatar = avatar_url

        # 更新登录信息
        user.last_login_ip = request.remote_addr
        user.last_login_time = int(datetime.datetime.now().timestamp() * 1000)

        # 生成 token
        token = secrets.token_hex(16)
        expires_at = int(datetime.datetime.now().timestamp() * 1000) + 7 * 24 * 60 * 60 * 1000

        user_token = UserToken.query.filter_by(user_id=user.id).first()
        if user_token:
            user_token.token = token
            user_token.expires_at = expires_at
        else:
            user_token = UserToken(user_id=user.id, token=token, expires_at=expires_at)
            db.session.add(user_token)

        db.session.commit()

        # 查询角色
        role = Role.query.filter_by(id=user.role_id, deleted=0).first()

        response = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "password": "",
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
