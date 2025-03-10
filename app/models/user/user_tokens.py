"""
用户令牌数据模型
定义UserTokens数据库表结构
"""

import datetime

from app.extensions import db


class UserToken(db.Model):
    """UserToken模型"""

    __tablename__ = "user_tokens"

    # 定义主键和外键
    # PRIMARY KEY (user_id, token),
    # FOREIGN KEY (user_id) REFERENCES users(id)

    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), primary_key=True, comment="用户ID"
    )
    token = db.Column(db.String(255), primary_key=True, comment="令牌")
    expires_at = db.Column(db.BigInteger, nullable=False, comment="过期时间戳")

    # 添加关系属性（可选）
    user = db.relationship("User", backref=db.backref("tokens", lazy=True))

    def __init__(self, **kwargs):
        """初始化UserToken实例"""
        super().__init__(**kwargs)
        if not self.expires_at:
            # 过期时间设置为7天
            self.expires_at = int(datetime.datetime.now().timestamp()) + 7 * 24 * 60 * 60
        if not self.user_id:
            raise ValueError("User ID is required")
        if not self.token:
            raise ValueError("Token is required")

    def __repr__(self):
        return f"<UserToken {self.user_id} - {self.token}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "userId": self.user_id,
            "token": self.token,
            "expiresAt": self.expires_at,
        }
