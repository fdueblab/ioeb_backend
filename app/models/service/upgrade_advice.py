"""服务升级建议模型。"""

import datetime
import uuid

from app.extensions import db


class ServiceUpgradeAdvice(db.Model):
    """用户成果的升级建议（三段论）"""

    __tablename__ = "service_upgrade_advices"

    id = db.Column(db.String(36), primary_key=True, comment="记录ID")
    service_id = db.Column(
        db.String(36),
        nullable=False,
        unique=True,
        index=True,
        comment="关联服务ID",
    )
    leading_analysis = db.Column(db.Text, nullable=True, comment="领先情况分析")
    auto_upgrade_suggestion = db.Column(db.Text, nullable=True, comment="自动升级建议")
    manual_update_suggestion = db.Column(db.Text, nullable=True, comment="人工更新建议")
    generated_at = db.Column(db.BigInteger, nullable=True, comment="生成时间 ms")
    generator_user_id = db.Column(
        db.String(36), nullable=True, index=True, comment="触发生成的用户ID"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.generated_at:
            self.generated_at = int(datetime.datetime.now().timestamp() * 1000)

    def to_dict(self):
        return {
            "leadingAnalysis": self.leading_analysis or "",
            "autoUpgradeSuggestion": self.auto_upgrade_suggestion or "",
            "manualUpdateSuggestion": self.manual_update_suggestion or "",
            "generatedAt": self.generated_at,
            "generatorUserId": self.generator_user_id,
        }

