"""
用户服务模块
处理用户相关的业务逻辑
"""

from typing import Dict, List, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError

from app.repositories.user_repository import UserRepository


class UserServiceError(Exception):
    """用户服务错误"""


class UserService:
    """用户服务类"""

    def __init__(self):
        """初始化用户服务"""
        self.user_repository = UserRepository()

    def get_all_users(self) -> List[Dict]:
        """
        获取所有用户

        Returns:
            List[Dict]: 用户列表，每个用户以字典形式表示
        """
        try:
            return self.user_repository.get_all_users_with_dict()
        except Exception as e:
            raise UserServiceError(f"获取用户列表失败: {str(e)}")

    def get_user_by_id(self, user_id: int) -> Dict:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID

        Returns:
            Dict: 用户信息字典

        Raises:
            UserServiceError: 用户不存在时抛出
        """
        try:
            user_dict = self.user_repository.get_user_dict_by_id(user_id)
            if not user_dict:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return user_dict
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"获取用户失败: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        根据邮箱获取用户

        Args:
            email: 用户邮箱

        Returns:
            Optional[Dict]: 用户信息字典，如果用户不存在则返回None
        """
        try:
            user = self.user_repository.find_by_email(email)
            if user:
                return user.to_dict()
            return None
        except Exception as e:
            raise UserServiceError(f"查询用户失败: {str(e)}")

    def create_user(self, username: str, email: str) -> Tuple[Dict, bool]:
        """
        创建新用户

        Args:
            username: 用户名
            email: 邮箱

        Returns:
            Tuple[Dict, bool]: 用户信息字典和是否为新创建的用户

        Raises:
            UserServiceError: 创建过程中出错
        """
        if not username or not email:
            raise UserServiceError("用户名和邮箱不能为空")

        try:
            # 检查用户是否已存在
            existing_user = self.user_repository.find_by_email(email)
            if existing_user:
                return existing_user.to_dict(), False

            # 创建新用户
            new_user = self.user_repository.create_user(username, email)
            return new_user.to_dict(), True
        except SQLAlchemyError as e:
            raise UserServiceError(f"创建用户失败: {str(e)}")
        except Exception as e:
            raise UserServiceError(f"创建用户过程中出错: {str(e)}")


# 创建单例实例，方便导入使用
user_service = UserService()
