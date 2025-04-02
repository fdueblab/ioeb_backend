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
    attribute = db.Column(db.Integer, nullable=False, comment="服务属性")
    type = db.Column(db.Integer, nullable=False, comment="服务类型")
    domain = db.Column(db.Integer, nullable=False, comment="领域")
    industry = db.Column(db.Integer, nullable=False, comment="行业")
    scenario = db.Column(db.Integer, nullable=False, comment="场景")
    technology = db.Column(db.Integer, nullable=False, comment="技术")

    # 部署信息
    network = db.Column(db.String(50), nullable=False, comment="网络类型")
    port = db.Column(db.String(100), nullable=False, comment="端口映射")
    volume = db.Column(db.String(200), nullable=False, comment="数据卷映射")

    # 状态信息
    status = db.Column(db.Integer, nullable=False, comment="服务状态")
    number = db.Column(db.String(50), nullable=False, comment="服务编号")
    deleted = db.Column(db.Integer, nullable=False, default=0, comment="是否删除：0-未删除，1-已删除")

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
        return {
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
            "apiList": [api.to_dict() for api in self.apis]
        }


class ServiceNorm(db.Model):
    """服务规范评分模型"""

    __tablename__ = "service_norms"

    id = db.Column(db.String(36), primary_key=True, comment="规范ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="关联的服务ID")
    key = db.Column(db.Integer, nullable=False, comment="规范类型")
    score = db.Column(db.Integer, nullable=False, comment="评分")

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "key": self.key,
            "score": self.score
        }


class ServiceSource(db.Model):
    """服务来源信息模型"""

    __tablename__ = "service_sources"

    id = db.Column(db.String(36), primary_key=True, comment="来源ID")
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, comment="关联的服务ID")
    popover_title = db.Column(db.String(100), nullable=False, comment="弹出框标题")
    company_name = db.Column(db.String(100), nullable=False, comment="公司名称")
    company_address = db.Column(db.String(200), nullable=False, comment="公司地址")
    company_contact = db.Column(db.String(50), nullable=False, comment="公司联系方式")
    company_introduce = db.Column(db.Text, nullable=False, comment="公司介绍")
    ms_introduce = db.Column(db.Text, nullable=False, comment="微服务介绍")
    company_score = db.Column(db.Integer, nullable=False, comment="公司评分")
    ms_score = db.Column(db.Integer, nullable=False, comment="微服务评分")

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "popoverTitle": self.popover_title,
            "companyName": self.company_name,
            "companyAddress": self.company_address,
            "companyContact": self.company_contact,
            "companyIntroduce": self.company_introduce,
            "msIntroduce": self.ms_introduce,
            "companyScore": self.company_score,
            "msScore": self.ms_score
        }


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