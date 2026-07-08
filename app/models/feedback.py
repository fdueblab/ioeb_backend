"""
意见反馈模型
用于保存用户提交的平台使用感受、建议和问题。
"""

import datetime
import uuid

from sqlalchemy import inspect, text

from app.extensions import db

DISPLAY_STATUS_MAP = {
    "open": "待处理",
    "processing": "处理中",
    "closed": "已回复",
}


class Feedback(db.Model):
    """用户意见反馈"""

    __tablename__ = "platform_feedbacks"

    id = db.Column(db.String(36), primary_key=True, comment="反馈ID")
    user_id = db.Column(db.String(36), nullable=True, index=True, comment="用户ID")
    username = db.Column(db.String(100), nullable=True, index=True, comment="用户名")
    feedback_type = db.Column(
        db.String(50), nullable=False, index=True, comment="反馈类型"
    )
    title = db.Column(db.String(100), nullable=False, comment="反馈标题")
    content = db.Column(db.Text, nullable=False, comment="反馈内容")
    contact = db.Column(db.String(100), nullable=True, comment="联系方式")
    status = db.Column(
        db.String(20),
        nullable=False,
        default="open",
        index=True,
        comment="状态：open-待处理，processing-处理中，closed-已回复",
    )
    response_summary = db.Column(db.Text, nullable=True, comment="平台处理总结")
    responded_at = db.Column(
        db.BigInteger, nullable=True, index=True, comment="平台回复时间"
    )
    feishu_status = db.Column(
        db.String(50), nullable=True, comment="飞书处理状态原文"
    )
    feishu_record_id = db.Column(
        db.String(100), nullable=True, comment="飞书多维表格记录ID"
    )
    feishu_sync_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True,
        comment="飞书同步状态：pending/synced/failed",
    )
    feishu_sync_error = db.Column(db.Text, nullable=True, comment="飞书同步错误")
    feishu_synced_at = db.Column(
        db.BigInteger, nullable=True, index=True, comment="飞书同步时间"
    )
    created_at = db.Column(db.BigInteger, nullable=False, index=True, comment="创建时间")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = int(datetime.datetime.now().timestamp() * 1000)

    @staticmethod
    def get_display_status(status):
        return DISPLAY_STATUS_MAP.get(status or "open", "待处理")

    @staticmethod
    def status_to_feishu_label(status, feishu_status=None):
        if feishu_status:
            return feishu_status
        mapping = {
            "open": "待处理",
            "processing": "处理中",
            "closed": "已处理",
        }
        return mapping.get(status or "open", "待处理")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.username,
            "feedbackType": self.feedback_type,
            "title": self.title,
            "content": self.content,
            "contact": self.contact,
            "status": self.status,
            "displayStatus": self.get_display_status(self.status),
            "responseSummary": self.response_summary,
            "respondedAt": self.responded_at,
            "feishuStatus": self.feishu_status,
            "feishuRecordId": self.feishu_record_id,
            "feishuSyncStatus": self.feishu_sync_status,
            "feishuSyncError": self.feishu_sync_error,
            "feishuSyncedAt": self.feishu_synced_at,
            "createdAt": self.created_at,
        }


def ensure_feedback_table():
    table_name = Feedback.__tablename__
    Feedback.__table__.create(db.engine, checkfirst=True)
    inspector = inspect(db.engine)
    if table_name not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    missing_columns = {
        "feishu_record_id": "VARCHAR(100)",
        "feishu_sync_status": "VARCHAR(20)",
        "feishu_sync_error": "TEXT",
        "feishu_synced_at": "BIGINT",
        "response_summary": "TEXT",
        "responded_at": "BIGINT",
        "feishu_status": "VARCHAR(50)",
    }
    for column_name, column_type in missing_columns.items():
        if column_name not in existing_columns:
            db.session.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            )
    db.session.commit()
