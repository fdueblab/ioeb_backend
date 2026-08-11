"""
成果消息模型
定义成果相关的消息表结构
"""

import datetime

from app.extensions import db


class ServiceMessage(db.Model):
    """成果消息模型"""

    __tablename__ = "service_messages"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 消息基本信息
    service_id = db.Column(db.String(36), nullable=False, comment="成果ID")
    sender_id = db.Column(db.String(36), nullable=False, comment="发送者ID")
    receiver_id = db.Column(db.String(36), nullable=False, comment="接收者ID")
    message_type = db.Column(
        db.String(20),
        nullable=False,
        comment="消息类型：contact_purchase-购买联系/use_service-使用服务/general-普通消息"
    )
    content = db.Column(db.Text, nullable=False, comment="消息内容")

    # 消息状态
    is_read = db.Column(db.Boolean, default=False, comment="是否已读")

    # 时间戳
    create_time = db.Column(
        db.BigInteger,
        nullable=False,
        comment="创建时间戳"
    )

    def __init__(self, **kwargs):
        """初始化ServiceMessage实例"""
        super().__init__(**kwargs)
        if not self.create_time:
            self.create_time = int(datetime.datetime.now().timestamp() * 1000)

    def __repr__(self):
        return f"<ServiceMessage id={self.id} type={self.message_type}>"

    def to_dict(self, include_relations=False):
        """将模型转换为字典

        Args:
            include_relations: 是否包含关联的 serviceName/senderName/receiverName。
                              为避免 N+1 查询，列表场景应由 service 层批量补充。
        """
        data = {
            "id": self.id,
            "serviceId": self.service_id,
            "senderId": self.sender_id,
            "receiverId": self.receiver_id,
            "messageType": self.message_type,
            "content": self.content,
            "isRead": self.is_read,
            "createTime": self.create_time,
            # 名称字段默认为空字符串，由 service 层批量补充
            "serviceName": "",
            "senderName": "",
            "receiverName": "",
        }

        if include_relations:
            # 延迟导入，避免循环依赖
            from app.models.service.service import Service
            from app.models.user import User

            service = Service.query.get(self.service_id)
            if service:
                data["serviceName"] = service.name

            sender = User.query.get(self.sender_id) if self.sender_id else None
            if sender:
                data["senderName"] = getattr(sender, "name", None) or getattr(sender, "username", None) or getattr(sender, "account", "") or ""

            receiver = User.query.get(self.receiver_id) if self.receiver_id else None
            if receiver:
                data["receiverName"] = getattr(receiver, "name", None) or getattr(receiver, "username", None) or getattr(receiver, "account", "") or ""

        return data