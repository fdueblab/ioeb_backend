"""
成果更新策略数据模型
定义 service_update_strategies 数据库表结构
"""

import datetime
from app.extensions import db


class ServiceUpdateStrategy(db.Model):
    """成果更新策略模型"""

    __tablename__ = "service_update_strategies"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="策略ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="成果ID")
    
    # 自动测试配置
    auto_test_enabled = db.Column(db.Boolean, default=False, comment="是否启用自动测试")
    auto_test_period = db.Column(db.Integer, default=0, comment="自动测试周期（天）")
    
    # 更新策略配置
    update_strategy_type = db.Column(db.String(50), default="manual", comment="更新策略类型：manual/auto/scheduled")
    update_config = db.Column(db.Text, nullable=True, comment="更新策略详细配置（JSON格式）")
    
    # 时间信息
    next_test_time = db.Column(db.Integer, nullable=True, comment="下次测试时间戳")
    last_test_time = db.Column(db.Integer, nullable=True, comment="上次测试时间戳")
    create_time = db.Column(db.Integer, nullable=False, comment="创建时间戳")
    update_time = db.Column(db.Integer, nullable=False, comment="更新时间戳")
    
    # 状态
    status = db.Column(db.Integer, default=1, comment="状态：1-正常，0-禁用")

    def __init__(self, **kwargs):
        """初始化"""
        super().__init__(**kwargs)
        current_time = int(datetime.datetime.now().timestamp() * 1000)
        if not self.create_time:
            self.create_time = current_time
        if not self.update_time:
            self.update_time = current_time

    def __repr__(self):
        return f"<ServiceUpdateStrategy {self.service_id} - {self.update_strategy_type}>"

    def to_dict(self):
        """将模型转换为字典"""
        import json
        
        config_dict = {}
        if self.update_config:
            try:
                config_dict = json.loads(self.update_config)
            except:
                pass
        
        return {
            "id": self.id,
            "serviceId": self.service_id,
            "autoTestEnabled": self.auto_test_enabled,
            "autoTestPeriod": self.auto_test_period,
            "updateStrategyType": self.update_strategy_type,
            "updateConfig": config_dict,
            "nextTestTime": self.next_test_time,
            "lastTestTime": self.last_test_time,
            "createTime": self.create_time,
            "updateTime": self.update_time,
            "status": self.status
        }