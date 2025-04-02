"""
服务来源信息模型
定义服务来源信息表结构
"""

from app.extensions import db


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