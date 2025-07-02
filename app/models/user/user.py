"""
用户数据模型
定义与Users数据库表结构
"""

import datetime

from app.extensions import db


class User(db.Model):
    """User模型"""

    __tablename__ = "users"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True)  # 使用字符串类型的UUID
    username = db.Column(db.String(100), unique=True, nullable=False, comment="用户登录名")
    name = db.Column(db.String(100), nullable=False, comment="用户姓名")
    password = db.Column(db.String(255), nullable=False, comment="加密后的密码")

    # 可选信息
    avatar = db.Column(db.String(255), nullable=True, comment="头像路径")
    telephone = db.Column(db.String(20), nullable=True, comment="电话号码")
    merchant_code = db.Column(db.String(50), nullable=True, comment="商户代码")
    role_id = db.Column(db.String(36), nullable=False, comment="角色ID，关联roles表")

    # 状态信息
    status = db.Column(db.Integer, nullable=False, default=1, comment="用户状态：1-正常，0-禁用")
    deleted = db.Column(
        db.Integer, nullable=False, default=0, comment="是否删除：0-未删除，1-已删除"
    )

    # 登录相关
    last_login_ip = db.Column(db.String(50), nullable=True, comment="最后登录IP")
    last_login_time = db.Column(db.BigInteger, nullable=True, comment="最后登录时间戳")

    # 创建和更新信息
    create_time = db.Column(db.BigInteger, nullable=False, comment="创建时间戳")
    creator_id = db.Column(db.String(36), nullable=True, comment="创建者ID")

    def __init__(self, **kwargs):
        """初始化用户实例"""
        super().__init__(**kwargs)
        if not self.create_time:
            self.create_time = int(datetime.datetime.now().timestamp() * 1000) # 毫秒时间戳
        if not self.id:
            import uuid

            self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "avatar": self.avatar,
            "telephone": self.telephone,
            "merchantCode": self.merchant_code,
            "roleId": self.role_id,
            "status": self.status,
            "deleted": self.deleted,
            "lastLoginIp": self.last_login_ip,
            "lastLoginTime": self.last_login_time,
            "createTime": self.create_time,
            "creatorId": self.creator_id,
        }
