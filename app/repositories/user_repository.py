"""
用户数据访问仓库
处理用户相关的数据库操作
"""

from typing import Dict, List, Optional

from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问仓库"""

    def __init__(self):
        """初始化用户仓库"""
        super().__init__(User)

    def find_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱查找用户

        Args:
            email: 用户邮箱

        Returns:
            User: 找到的用户，如果不存在则返回None
        """
        return self.find_one_by(email=email)

    def find_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名查找用户

        Args:
            username: 用户名

        Returns:
            User: 找到的用户，如果不存在则返回None
        """
        return self.find_one_by(username=username)

    def create_user(self, username: str, name: str) -> User:
        """
        创建新用户

        Args:
            username: 用户名
            name: 用户姓名

        Returns:
            User: 创建的用户
        """
        return self.create(username=username, name=name)

    def get_all_users_with_dict(self) -> List[Dict]:
        """
        获取所有用户（字典格式）

        Returns:
            List[Dict]: 用户字典列表
        """
        users = self.get_all()
        return [user.to_dict() for user in users]

    def get_user_dict_by_id(self, user_id: str) -> Optional[Dict]:
        """
        根据ID获取用户字典

        Args:
            user_id: 用户ID（UUID字符串）

        Returns:
            Dict: 用户字典，如果不存在则返回None
        """
        user = self.get_by_id(user_id)
        if user:
            return user.to_dict()
        return None
