"""
微服务基本信息模型
定义微服务的基本信息表结构
"""

import datetime
import json

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
    port = db.Column(db.String(500), nullable=False, comment="端口映射")
    volume = db.Column(db.String(500), nullable=False, comment="数据卷映射")

    # 状态信息
    status = db.Column(db.String(50), nullable=False, comment="服务状态")
    number = db.Column(db.Integer, nullable=False, default=0, comment="服务调用次数")
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
            self.create_time = int(datetime.datetime.now().timestamp() * 1000) # 毫秒时间戳
        if not self.id:
            raise ValueError("Service ID is required")

    def __repr__(self):
        return f"<Service {self.name}>"

    def to_dict(self):
        """将模型转换为字典"""
        base_dict = {
            "id": self.id,
            "name": self.name,
            "attribute": self.attribute,
            "type": self.type,
            "domain": self.domain,
            "industry": self.industry,
            "scenario": self.scenario,
            "technology": self.technology,
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
        }
        
        # 对于MCP类型的服务，使用扁平化的格式 + apiList（兼容旧版）
        if self.type == 'atomic_mcp':
            # 从第一个API中提取url、des、method、tools、isFake和exampleMsg
            if self.apis and len(self.apis) > 0:
                first_api = self.apis[0]
                base_dict["url"] = first_api.url
                base_dict["des"] = first_api.des or ""
                base_dict["method"] = first_api.method
                base_dict["isFake"] = 1 if first_api.is_fake else 0
                # 提取tools列表
                base_dict["tools"] = [tool.to_dict() for tool in first_api.tools]
                # 提取示例消息
                if first_api.example_msg:
                    try:
                        base_dict["exampleMsg"] = json.loads(first_api.example_msg)
                    except json.JSONDecodeError:
                        # 如果不是有效JSON，则返回原始字符串
                        base_dict["exampleMsg"] = first_api.example_msg
                else:
                    base_dict["exampleMsg"] = []
                # 同时保留apiList格式以兼容旧版前端
                base_dict["apiList"] = [api.to_dict() for api in self.apis]
            else:
                # 如果没有API，提供默认值
                base_dict["url"] = ""
                base_dict["des"] = ""
                base_dict["method"] = "sse"
                base_dict["isFake"] = 0
                base_dict["tools"] = []
                base_dict["exampleMsg"] = []
                base_dict["apiList"] = []
        else:
            # 对于REST类型的服务，保持原有的apiList格式
            base_dict["apiList"] = [api.to_dict() for api in self.apis]
        
        return base_dict
