"""
成果更新历史数据模型
记录每次更新的结果
"""

import datetime
from app.extensions import db


class ServiceUpdateHistory(db.Model):
    """成果更新历史模型"""

    __tablename__ = "service_update_histories"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="更新记录ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="成果ID")

    # 更新信息
    update_type = db.Column(db.String(50), default="manual", comment="更新类型：manual/auto/scheduled")
    update_status = db.Column(db.String(20), default="pending", comment="更新状态：pending/success/failed/error")
    update_reason = db.Column(db.Text, nullable=True, comment="更新原因")
    update_result = db.Column(db.Text, nullable=True, comment="更新结果详情（JSON格式）")

    # 版本信息
    version_before = db.Column(db.String(50), nullable=True, comment="更新前版本")
    version_after = db.Column(db.String(50), nullable=True, comment="更新后版本")

    # 时间信息
    update_time = db.Column(db.Integer, nullable=False, comment="更新时间戳")
    duration = db.Column(db.Integer, nullable=True, comment="更新耗时（毫秒）")

    def __init__(self, **kwargs):
        """初始化"""
        super().__init__(**kwargs)
        if not self.update_time:
            self.update_time = int(datetime.datetime.now().timestamp() * 1000)

    def __repr__(self):
        return f"<ServiceUpdateHistory {self.service_id} - {self.update_status}>"

    def to_dict(self):
        """将模型转换为字典"""
        import json

        result_dict = {}
        if self.update_result:
            try:
                result_dict = json.loads(self.update_result)
            except:
                pass

        return {
            "id": self.id,
            "serviceId": self.service_id,
            "updateType": self.update_type,
            "updateStatus": self.update_status,
            "updateReason": self.update_reason,
            "updateResult": result_dict,
            "versionBefore": self.version_before,
            "versionAfter": self.version_after,
            "updateTime": self.update_time,
            "duration": self.duration
        }