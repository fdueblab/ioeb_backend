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
    # 元应用专用字段
    input_name = db.Column(db.String(100), nullable=True, comment="输入名称")
    output_name = db.Column(db.String(100), nullable=True, comment="输出名称")
    output_visualization = db.Column(db.Boolean, default=False, comment="是否可视化输出")
    submit_button_text = db.Column(db.String(50), nullable=True, comment="提交按钮文本")

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
                try:
                    result["response"] = json.loads(self.response)
                except json.JSONDecodeError:
                    # 如果响应不是有效JSON，则返回原始字符串
                    result["response"] = self.response
            if self.response_file_name:
                result["responseFileName"] = self.response_file_name
        
        # 添加元应用相关字段
        if self.input_name:
            result["inputName"] = self.input_name
        if self.output_name:
            result["outputName"] = self.output_name
        if self.output_visualization:
            result["outputVisualization"] = self.output_visualization
        if self.submit_button_text:
            result["submitButtonText"] = self.submit_button_text

        if self.parameters:
            result["parameters"] = [param.to_dict() for param in self.parameters]

        return result 