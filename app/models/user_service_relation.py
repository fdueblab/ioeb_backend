"""
用户与成果关系模型
定义用户与成果之间的关系表结构
"""

import datetime

from app.extensions import db


class UserServiceRelation(db.Model):
    """用户与成果关系模型"""

    __tablename__ = "user_service_relations"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 关系信息
    user_id = db.Column(db.String(36), nullable=False, comment="用户ID")
    service_id = db.Column(db.String(36), nullable=False, comment="成果ID")
    relation_type = db.Column(
        db.String(20),
        nullable=False,
        comment="关系类型：developed-已开发/purchased-已购买/interested-感兴趣"
    )

    # 购买信息（仅对已购买成果）
    purchase_time = db.Column(db.BigInteger, comment="购买时间戳")
    purchase_price = db.Column(db.Float, comment="购买价格")

    # 时间戳
    create_time = db.Column(
        db.BigInteger,
        nullable=False,
        comment="创建时间戳"
    )

    def __init__(self, **kwargs):
        """初始化UserServiceRelation实例"""
        super().__init__(**kwargs)
        if not self.create_time:
            self.create_time = int(datetime.datetime.now().timestamp() * 1000)

    def __repr__(self):
        return f"<UserServiceRelation user={self.user_id} service={self.service_id} type={self.relation_type}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "serviceId": self.service_id,
            "relationType": self.relation_type,
            "purchaseTime": self.purchase_time,
            "purchasePrice": self.purchase_price,
            "createTime": self.create_time,
        }