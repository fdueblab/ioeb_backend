"""
用户与成果关系服务
提供用户与成果关系的管理功能
"""

from app.extensions import db
from app.models.user_service_relation import UserServiceRelation
from app.models.service.service import Service


class UserServiceRelationError(Exception):
    """用户成果关系服务错误"""
    pass


class UserServiceRelationService:
    """用户成果关系服务类"""

    @staticmethod
    def get_user_services_by_relation(user_id, relation_type):
        """
        获取用户的指定类型成果列表

        Args:
            user_id: 用户ID
            relation_type: 关系类型 (developed/purchased/interested)

        Returns:
            list: 成果列表
        """
        try:
            # 查询用户与成果的关系
            relations = UserServiceRelation.query.filter_by(
                user_id=user_id,
                relation_type=relation_type
            ).all()

            # 获取成果详情
            service_ids = [r.service_id for r in relations]
            services = Service.query.filter(Service.id.in_(service_ids)).all()

            # 创建service_id到service的映射
            service_map = {s.id: s for s in services}

            # 组装结果
            result = []
            for relation in relations:
                service = service_map.get(relation.service_id)
                if service:
                    service_dict = service.to_list_dict()
                    service_dict['relation'] = relation.to_dict()
                    result.append(service_dict)

            return result

        except Exception as e:
            raise UserServiceRelationError(f"获取用户成果列表失败: {str(e)}")

    @staticmethod
    def add_service_relation(user_id, service_id, relation_type):
        """
        添加成果关系

        Args:
            user_id: 用户ID
            service_id: 成果ID
            relation_type: 关系类型

        Returns:
            UserServiceRelation: 关系对象
        """
        try:
            # 检查是否已存在
            existing = UserServiceRelation.query.filter_by(
                user_id=user_id,
                service_id=service_id,
                relation_type=relation_type
            ).first()

            if existing:
                return existing

            # 创建新关系
            relation = UserServiceRelation(
                user_id=user_id,
                service_id=service_id,
                relation_type=relation_type
            )

            db.session.add(relation)
            db.session.commit()

            return relation

        except Exception as e:
            db.session.rollback()
            raise UserServiceRelationError(f"添加成果关系失败: {str(e)}")

    @staticmethod
    def remove_service_relation(user_id, service_id, relation_type=None):
        """
        删除成果关系

        Args:
            user_id: 用户ID
            service_id: 成果ID
            relation_type: 关系类型（可选，如果提供则只删除指定类型的关系）

        Returns:
            bool: 是否成功删除
        """
        try:
            query = UserServiceRelation.query.filter_by(
                user_id=user_id,
                service_id=service_id
            )

            if relation_type:
                query = query.filter_by(relation_type=relation_type)

            count = query.delete()
            db.session.commit()

            return count > 0

        except Exception as e:
            db.session.rollback()
            raise UserServiceRelationError(f"删除成果关系失败: {str(e)}")

    @staticmethod
    def check_user_service_relation(user_id, service_id, relation_type):
        """
        检查用户是否与成果有指定关系

        Args:
            user_id: 用户ID
            service_id: 成果ID
            relation_type: 关系类型

        Returns:
            bool: 是否存在关系
        """
        relation = UserServiceRelation.query.filter_by(
            user_id=user_id,
            service_id=service_id,
            relation_type=relation_type
        ).first()

        return relation is not None


# 创建全局实例
user_service_relation_service = UserServiceRelationService()