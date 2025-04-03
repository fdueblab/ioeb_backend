"""
服务API信息模型
定义服务API信息表结构
"""

import json

from app.extensions import db


class ServiceApi(db.Model):
    """服务API信息模型"""

    __tablename__ = "service_apis"

    id = db.Column(db.String(36), primary_key=True, comment="API ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="关联的服务ID")
    name = db.Column(db.String(100), nullable=False, comment="API名称")
    url = db.Column(db.String(200), nullable=False, comment="API地址")
    method = db.Column(db.String(10), nullable=False, comment="请求方法")
    des = db.Column(db.Text, nullable=True, comment="API描述")
    parameter_type = db.Column(db.Integer, nullable=False, comment="参数类型")
    response_type = db.Column(db.Integer, nullable=False, comment="响应类型")
    is_fake = db.Column(db.Boolean, default=False, comment="是否为模拟数据")
    response = db.Column(db.Text, nullable=True, comment="模拟响应数据")
    response_file_name = db.Column(db.String(100), nullable=True, comment="响应文件名")

    # 关联关系
    parameters = db.relationship("ServiceApiParameter", backref="api", lazy=True)

    def to_dict(self):
        """将模型转换为字典"""
        result = {
            "name": self.name,
            "url": self.url,
            "method": self.method,
            "des": self.des,
            "parameterType": self.parameter_type,
            "responseType": self.response_type
        }

        if self.is_fake:
            result["isFake"] = True
            if self.response:
                result["response"] = json.loads(self.response)
            if self.response_file_name:
                result["responseFileName"] = self.response_file_name

        if self.parameters:
            result["parameters"] = [param.to_dict() for param in self.parameters]

        return result 