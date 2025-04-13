"""
微服务基本信息模型
定义微服务的基本信息表结构
"""

import datetime

from app.extensions import db


class Service(db.Model):
    """微服务基本信息模型"""

    __tablename__ = "services"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="服务ID")
    name = db.Column(db.String(100), nullable=False, comment="服务名称")
    attribute = db.Column(db.String(50), nullable=False, comment="服务属性")
    type = db.Column(db.String(50), nullable=False, comment="服务类型")
    domain = db.Column(db.String(50), nullable=False, comment="领域")
    industry = db.Column(db.String(50), nullable=False, comment="行业")
    scenario = db.Column(db.String(50), nullable=False, comment="场景")
    technology = db.Column(db.String(50), nullable=False, comment="技术")

    # 部署信息
    network = db.Column(db.String(50), nullable=False, comment="网络类型")
    port = db.Column(db.String(100), nullable=False, comment="端口映射")
    volume = db.Column(db.String(200), nullable=False, comment="数据卷映射")

    # 状态信息
    status = db.Column(db.String(50), nullable=False, comment="服务状态")
    number = db.Column(db.String(50), nullable=False, comment="服务编号")
    deleted = db.Column(
        db.Integer, nullable=False, default=0, comment="是否删除：0-未删除，1-已删除"
    )

    # 创建和更新信息
    create_time = db.Column(db.BigInteger, nullable=False, comment="创建时间戳")
    creator_id = db.Column(db.String(36), nullable=True, comment="创建者ID")

    # 关联关系
    norms = db.relationship("ServiceNorm", backref="service", lazy=True)
    source = db.relationship("ServiceSource", backref="service", uselist=False)
    apis = db.relationship("ServiceApi", backref="service", lazy=True)

    def __init__(self, **kwargs):
        """初始化Service实例"""
        super().__init__(**kwargs)
        if not self.create_time:
            self.create_time = int(datetime.datetime.now().timestamp())
        if not self.id:
            raise ValueError("Service ID is required")

    def __repr__(self):
        return f"<Service {self.name}>"

    def to_dict(self):
        """将模型转换为字典"""
        # 尝试将字段转换为数字
        try:
            industry = int(self.industry)
        except (ValueError, TypeError):
            industry = self.industry
            
        try:
            scenario = int(self.scenario)
        except (ValueError, TypeError):
            scenario = self.scenario
            
        try:
            technology = int(self.technology)
        except (ValueError, TypeError):
            technology = self.technology
        
        return {
            "id": self.id,
            "name": self.name,
            "attribute": self.attribute,
            "type": self.type,
            "domain": self.domain,
            "industry": industry,
            "scenario": scenario,
            "technology": technology,
            "network": self.network,
            "port": self.port,
            "volume": self.volume,
            "status": self.status,
            "number": self.number,
            "deleted": self.deleted,
            "createTime": self.create_time,
            "creatorId": self.creator_id,
            "norm": [norm.to_dict() for norm in self.norms],
            "source": self.source.to_dict() if self.source else None,
            "apiList": [api.to_dict() for api in self.apis],
        }
