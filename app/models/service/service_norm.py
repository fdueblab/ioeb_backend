"""
服务规范评分模型
定义服务规范评分表结构
"""

from app.extensions import db


class ServiceNorm(db.Model):
    """服务规范评分模型"""

    __tablename__ = "service_norms"

    id = db.Column(db.String(36), primary_key=True, comment="规范ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="关联的服务ID")
    key = db.Column(db.String(50), nullable=False, comment="规范类型")
    score = db.Column(db.Integer, nullable=False, comment="评分")

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "key": self.key,
            "score": self.score
        } 