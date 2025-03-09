"""
角色数据模型
定义Roles数据库表结构
"""

import datetime

from app.extensions import db


class Role(db.Model):
    """Role模型"""

    __tablename__ = "roles"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="角色ID")  # 使用字符串类型的UUID
    name = db.Column(db.String(100), unique=True, nullable=False, comment="角色名称")
    describe = db.Column(db.String(100), nullable=False, comment="角色描述")

    # 状态信息
    status = db.Column(db.Integer, nullable=False, default=1, comment="用户状态：1-正常，0-禁用")
    deleted = db.Column(
        db.Integer, nullable=False, default=0, comment="是否删除：0-未删除，1-已删除"
    )

    # 创建和更新信息
    create_time = db.Column(db.BigInteger, nullable=False, comment="创建时间戳")
    creator_id = db.Column(db.String(36), nullable=True, comment="创建者ID")

    def __init__(self, **kwargs):
        """初始化Role实例"""
        super().__init__(**kwargs)
        if not self.create_time:
            self.create_time = int(datetime.datetime.now().timestamp())
        if not self.id:
            raise ValueError("Role ID is required")

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "status": self.status,
            "deleted": self.deleted,
            "createTime": self.create_time,
            "creatorId": self.creator_id,
        }
