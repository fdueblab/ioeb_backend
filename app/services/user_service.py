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

    def get_user_by_id(self, user_id: str) -> Dict:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID（UUID字符串）

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

    def create_user(self, username: str, name: str, password: str) -> Tuple[Dict, bool]:
        """
        创建新用户

        Args:
            username: 用户名
            name: 用户姓名
            password: 用户密码

        Returns:
            Tuple[Dict, bool]: 用户信息字典和是否为新创建的用户

        Note:
            新创建的用户默认角色为"user"

        Raises:
            UserServiceError: 创建过程中出错
        """
        if not username or not name or not password:
            raise UserServiceError("用户名、姓名和密码不能为空")

        try:
            # 检查用户是否已存在（通过用户名检查）
            existing_user = self.user_repository.find_by_username(username)
            if existing_user:
                return existing_user.to_dict(), False

            # 创建新用户
            new_user = self.user_repository.create_user(username, name, password)
            return new_user.to_dict(), True
        except SQLAlchemyError as e:
            raise UserServiceError(f"创建用户失败: {str(e)}")
        except Exception as e:
            raise UserServiceError(f"创建用户过程中出错: {str(e)}")

    def update_user(self, user_id: str, data: Dict) -> Dict:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            data: 更新数据

        Returns:
            Dict: 更新后的用户信息字典

        Raises:
            UserServiceError: 用户不存在或更新失败
        """
        try:
            user = self.user_repository.update_user(user_id, data)
            if not user:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return user.to_dict()
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"更新用户失败: {str(e)}")

    def delete_user(self, user_id: str) -> bool:
        """
        删除用户（逻辑删除）

        Args:
            user_id: 用户ID

        Returns:
            bool: 删除是否成功

        Raises:
            UserServiceError: 用户不存在或删除失败
        """
        try:
            success = self.user_repository.delete_user(user_id)
            if not success:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return success
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"删除用户失败: {str(e)}")

    def update_user_status(self, user_id: str, status: int) -> bool:
        """
        更新用户状态

        Args:
            user_id: 用户ID
            status: 用户状态（1-正常，0-禁用）

        Returns:
            bool: 更新是否成功

        Raises:
            UserServiceError: 用户不存在或状态值无效
        """
        if status not in [0, 1]:
            raise UserServiceError("用户状态值无效，只能是0（禁用）或1（正常）")

        try:
            user = self.user_repository.update_user_status(user_id, status)
            if not user:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return True
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"更新用户状态失败: {str(e)}")

    def update_user_password(self, user_id: str, password: str) -> bool:
        """
        更新用户密码

        Args:
            user_id: 用户ID
            password: 新密码

        Returns:
            bool: 更新是否成功

        Raises:
            UserServiceError: 用户不存在或密码为空
        """
        if not password:
            raise UserServiceError("密码不能为空")

        try:
            user = self.user_repository.update_user_password(user_id, password)
            if not user:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return True
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"更新用户密码失败: {str(e)}")

    def update_user_role(self, user_id: str, role_id: str) -> bool:
        """
        更新用户角色

        Args:
            user_id: 用户ID
            role_id: 角色ID

        Returns:
            bool: 更新是否成功

        Raises:
            UserServiceError: 用户不存在或角色ID为空
        """
        if not role_id:
            raise UserServiceError("角色ID不能为空")

        try:
            user = self.user_repository.update_user_role(user_id, role_id)
            if not user:
                raise UserServiceError(f"用户ID {user_id} 不存在")
            return True
        except Exception as e:
            if isinstance(e, UserServiceError):
                raise
            raise UserServiceError(f"更新用户角色失败: {str(e)}")


# 创建单例实例，方便导入使用
user_service = UserService()
