"""
成果消息服务
提供成果相关消息的发送、查询和管理功能
"""

from app.extensions import db
from app.models.service_message import ServiceMessage
from app.models.service.service import Service


class ServiceMessageError(Exception):
    """成果消息服务错误"""
    pass


class ServiceMessageService:
    """成果消息服务类"""

    @staticmethod
    def _resolve_receiver_id(service_id, sender_id):
        """根据成果ID解析接收者ID（成果创建者）

        Args:
            service_id: 成果ID
            sender_id: 发送者ID（避免自己给自己发消息）

        Returns:
            str: 接收者ID（成果创建者ID），若创建者缺失则返回 None
        """
        service = Service.query.get(service_id)
        if not service:
            raise ServiceMessageError("成果不存在")

        creator_id = getattr(service, "creator_id", None)
        # 如果创建者就是发送者自己，仍然返回创建者ID，
        # 前端逻辑可据此判断"自己购买自己的成果"场景
        return creator_id

    @staticmethod
    def _enrich_messages(messages):
        """批量补充消息列表中的 serviceName/senderName/receiverName 字段

        为避免 N+1 查询，统一收集 ID 后批量查询。
        """
        if not messages:
            return []

        # 延迟导入 User，避免循环依赖
        try:
            from app.models.user.user import User
        except ImportError:
            User = None

        service_ids = set()
        user_ids = set()
        for msg in messages:
            if msg.service_id:
                service_ids.add(msg.service_id)
            if msg.sender_id:
                user_ids.add(msg.sender_id)
            if msg.receiver_id:
                user_ids.add(msg.receiver_id)

        # 批量查询服务名称
        service_name_map = {}
        if service_ids:
            services = Service.query.filter(Service.id.in_(service_ids)).all()
            service_name_map = {s.id: s.name for s in services}

        # 批量查询用户名称
        user_name_map = {}
        if user_ids and User is not None:
            users = User.query.filter(User.id.in_(user_ids)).all()
            for u in users:
                name = (
                    getattr(u, "name", None)
                    or getattr(u, "username", None)
                    or getattr(u, "account", None)
                    or ""
                )
                user_name_map[u.id] = name

        # 组装最终结果
        result = []
        for msg in messages:
            data = msg.to_dict()
            data["serviceName"] = service_name_map.get(msg.service_id, "")
            data["senderName"] = user_name_map.get(msg.sender_id, "")
            data["receiverName"] = user_name_map.get(msg.receiver_id, "")
            # 标记是否为当前用户发送的消息（前端据此区分气泡方向）
            result.append(data)
        return result

    @staticmethod
    def send_purchase_contact_message(sender_id, receiver_id, service_id, content):
        """发送购买联系消息

        Args:
            sender_id: 发送者ID
            receiver_id: 接收者ID（为 None 时自动取成果创建者）
            service_id: 成果ID
            content: 消息内容

        Returns:
            dict: 消息字典（含名称字段）
        """
        try:
            # 检查成果是否存在
            service = Service.query.get(service_id)
            if not service:
                raise ServiceMessageError("成果不存在")

            # 若未显式指定接收者，则取成果创建者
            actual_receiver_id = receiver_id or service.creator_id
            if not actual_receiver_id:
                raise ServiceMessageError("无法确定消息接收者：成果未关联创建者")

            message = ServiceMessage(
                service_id=service_id,
                sender_id=sender_id,
                receiver_id=actual_receiver_id,
                message_type="contact_purchase",
                content=content,
            )

            db.session.add(message)
            db.session.commit()

            # 返回包含名称信息的字典
            return ServiceMessageService._enrich_messages([message])[0]

        except ServiceMessageError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ServiceMessageError(f"发送购买联系消息失败: {str(e)}")

    @staticmethod
    def send_use_service_message(sender_id, receiver_id, service_id, content):
        """发送使用服务消息

        Args:
            sender_id: 发送者ID
            receiver_id: 接收者ID（为 None 时自动取成果创建者）
            service_id: 成果ID
            content: 消息内容

        Returns:
            dict: 消息字典（含名称字段）
        """
        try:
            service = Service.query.get(service_id)
            if not service:
                raise ServiceMessageError("成果不存在")

            actual_receiver_id = receiver_id or service.creator_id
            if not actual_receiver_id:
                raise ServiceMessageError("无法确定消息接收者：成果未关联创建者")

            message = ServiceMessage(
                service_id=service_id,
                sender_id=sender_id,
                receiver_id=actual_receiver_id,
                message_type="use_service",
                content=content,
            )

            db.session.add(message)
            db.session.commit()

            return ServiceMessageService._enrich_messages([message])[0]

        except ServiceMessageError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ServiceMessageError(f"发送使用服务消息失败: {str(e)}")

    @staticmethod
    def get_service_messages(service_id, user_id=None):
        """获取成果的消息列表

        Args:
            service_id: 成果ID
            user_id: 当前用户ID（可选，用于标记 isMine 字段）

        Returns:
            list: 消息字典列表
        """
        try:
            messages = ServiceMessage.query.filter_by(
                service_id=service_id
            ).order_by(ServiceMessage.create_time.asc()).all()

            result = ServiceMessageService._enrich_messages(messages)
            # 标记当前用户发送的消息
            if user_id:
                for item in result:
                    item["isMine"] = (item.get("senderId") == user_id)
            return result

        except Exception as e:
            raise ServiceMessageError(f"获取消息列表失败: {str(e)}")

    @staticmethod
    def reply_message(message_id, sender_id, content):
        """回复消息

        Args:
            message_id: 原消息ID
            sender_id: 回复者ID
            content: 回复内容

        Returns:
            dict: 新消息字典
        """
        try:
            original_message = ServiceMessage.query.get(message_id)
            if not original_message:
                raise ServiceMessageError("原消息不存在")

            # 回复消息的接收者为原消息发送者
            reply = ServiceMessage(
                service_id=original_message.service_id,
                sender_id=sender_id,
                receiver_id=original_message.sender_id,
                message_type="general",
                content=content,
            )

            db.session.add(reply)
            db.session.commit()

            return ServiceMessageService._enrich_messages([reply])[0]

        except ServiceMessageError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ServiceMessageError(f"回复消息失败: {str(e)}")

    @staticmethod
    def get_user_unread_messages(user_id):
        """获取用户未读消息列表

        Args:
            user_id: 用户ID

        Returns:
            list: 未读消息列表
        """
        try:
            messages = ServiceMessage.query.filter_by(
                receiver_id=user_id,
                is_read=False
            ).order_by(ServiceMessage.create_time.desc()).all()

            result = ServiceMessageService._enrich_messages(messages)
            # 标记当前用户发送的消息（未读消息都是发给当前用户的，isMine=False）
            for item in result:
                item["isMine"] = (item.get("senderId") == user_id)
            return result

        except Exception as e:
            raise ServiceMessageError(f"获取未读消息失败: {str(e)}")

    @staticmethod
    def mark_message_as_read(message_id, user_id=None):
        """标记消息为已读

        Args:
            message_id: 消息ID
            user_id: 当前用户ID（可选，用于权限校验）

        Returns:
            bool: 是否成功
        """
        try:
            message = ServiceMessage.query.get(message_id)
            if not message:
                raise ServiceMessageError("消息不存在")

            # 权限校验：只有接收者才能标记已读
            if user_id and message.receiver_id != user_id:
                raise ServiceMessageError("无权操作此消息")

            message.is_read = True
            db.session.commit()

            return True

        except ServiceMessageError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ServiceMessageError(f"标记消息失败: {str(e)}")


# 创建全局实例
service_message_service = ServiceMessageService()
