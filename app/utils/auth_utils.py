"""请求用户身份解析工具。"""

import datetime

from flask import g, request

from app.models.user.user import User
from app.models.user.user_tokens import UserToken


def get_request_user():
    user = getattr(g, "audit_user", None)
    if user:
        return user

    token = request.headers.get("Access-Token", "")
    if not token:
        return None

    user_token = UserToken.query.filter_by(token=token).first()
    if not user_token:
        return None

    now = int(datetime.datetime.now().timestamp() * 1000)
    if user_token.expires_at < now:
        return None

    return User.query.filter_by(id=user_token.user_id, deleted=0).first()
