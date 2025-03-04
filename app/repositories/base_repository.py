"""
基础数据访问仓库
提供通用的数据库CRUD操作
"""

from typing import Generic, List, Optional, Type, TypeVar, Union

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

# 定义泛型类型变量，用于表示ORM模型
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    基础数据访问仓库类
    提供对特定模型的通用CRUD操作
    """

    def __init__(self, model_class: Type[T]):
        """
        初始化仓库

        Args:
            model_class: ORM模型类
        """
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        """
        根据ID获取记录

        Args:
            id: 记录ID

        Returns:
            返回找到的记录，如果不存在则返回None
        """
        return self.model_class.query.get(id)

    def get_all(self) -> List[T]:
        """
        获取所有记录

        Returns:
            所有记录列表
        """
        return self.model_class.query.all()

    def find_by(self, **criteria) -> List[T]:
        """
        根据条件查找记录

        Args:
            **criteria: 过滤条件，如 name='test', age=18

        Returns:
            符合条件的记录列表
        """
        return self.model_class.query.filter_by(**criteria).all()

    def find_one_by(self, **criteria) -> Optional[T]:
        """
        根据条件查找单个记录

        Args:
            **criteria: 过滤条件，如 name='test', age=18

        Returns:
            符合条件的第一条记录，如果不存在则返回None
        """
        return self.model_class.query.filter_by(**criteria).first()

    def create(self, **data) -> Union[T, None]:
        """
        创建新记录

        Args:
            **data: 记录数据

        Returns:
            创建的记录，如果创建失败则返回None

        Raises:
            SQLAlchemyError: 数据库错误
        """
        try:
            entity = self.model_class(**data)
            db.session.add(entity)
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"创建记录失败: {str(e)}")
            raise

    def update(self, entity: T, **data) -> Union[T, None]:
        """
        更新记录

        Args:
            entity: 要更新的记录
            **data: 更新的数据

        Returns:
            更新后的记录，如果更新失败则返回None

        Raises:
            SQLAlchemyError: 数据库错误
        """
        try:
            for key, value in data.items():
                setattr(entity, key, value)
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"更新记录失败: {str(e)}")
            raise

    def delete(self, entity: T) -> bool:
        """
        删除记录

        Args:
            entity: 要删除的记录

        Returns:
            删除是否成功

        Raises:
            SQLAlchemyError: 数据库错误
        """
        try:
            db.session.delete(entity)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"删除记录失败: {str(e)}")
            raise

    def delete_by_id(self, id: int) -> bool:
        """
        根据ID删除记录

        Args:
            id: 记录ID

        Returns:
            删除是否成功

        Raises:
            SQLAlchemyError: 数据库错误
        """
        entity = self.get_by_id(id)
        if entity:
            return self.delete(entity)
        return False
