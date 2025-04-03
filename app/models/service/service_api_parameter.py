"""
服务API参数模型
定义服务API参数表结构
"""

from app.extensions import db


class ServiceApiParameter(db.Model):
    """服务API参数模型"""

    __tablename__ = "service_api_parameters"

    id = db.Column(db.String(36), primary_key=True, comment="参数ID")
    api_id = db.Column(db.String(36), db.ForeignKey("service_apis.id"), nullable=False, comment="关联的API ID")
    name = db.Column(db.String(100), nullable=False, comment="参数名称")
    type = db.Column(db.String(50), nullable=False, comment="参数类型")
    des = db.Column(db.Text, nullable=True, comment="参数描述")

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "des": self.des
        } 