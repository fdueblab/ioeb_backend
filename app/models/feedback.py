"""
意见反馈模型
用于保存用户提交的平台使用感受、建议和问题。
"""

import datetime
import uuid

from app.extensions import db


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
        comment="状态：open-待处理，closed-已处理",
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
            "feishuRecordId": self.feishu_record_id,
            "feishuSyncStatus": self.feishu_sync_status,
            "feishuSyncError": self.feishu_sync_error,
            "feishuSyncedAt": self.feishu_synced_at,
            "createdAt": self.created_at,
        }
