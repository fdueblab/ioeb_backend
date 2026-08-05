"""
成果测试历史数据模型
记录每次自动测试的结果
"""

import datetime
from app.extensions import db


class ServiceTestHistory(db.Model):
    """成果测试历史模型"""

    __tablename__ = "service_test_histories"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="测试记录ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="成果ID")

    # 测试结果
    test_type = db.Column(db.String(50), default="auto", comment="测试类型：auto/manual")
    test_status = db.Column(db.String(20), default="pending", comment="测试状态：pending/success/failed/error")
    test_result = db.Column(db.Text, nullable=True, comment="测试结果详情（JSON格式）")

    # 响应信息
    response_time = db.Column(db.Integer, nullable=True, comment="响应时间（毫秒）")
    status_code = db.Column(db.Integer, nullable=True, comment="HTTP状态码")

    # 时间信息
    test_time = db.Column(db.Integer, nullable=False, comment="测试时间戳")
    next_test_time = db.Column(db.Integer, nullable=True, comment="下次测试时间戳")

    def __init__(self, **kwargs):
        """初始化"""
        super().__init__(**kwargs)
        if not self.test_time:
            self.test_time = int(datetime.datetime.now().timestamp() * 1000)

    def __repr__(self):
        return f"<ServiceTestHistory {self.service_id} - {self.test_status}>"

    def to_dict(self):
        """将模型转换为字典"""
        import json

        result_dict = {}
        if self.test_result:
            try:
                result_dict = json.loads(self.test_result)
            except:
                pass

        return {
            "id": self.id,
            "serviceId": self.service_id,
            "testType": self.test_type,
            "testStatus": self.test_status,
            "testResult": result_dict,
            "responseTime": self.response_time,
            "statusCode": self.status_code,
            "testTime": self.test_time,
            "nextTestTime": self.next_test_time
        }