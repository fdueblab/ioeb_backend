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
            User: 找到的用户，如果不存在或已删除则返回None
        """
        return self.find_one_by(email=email, deleted=0)

    def find_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名查找用户

        Args:
            username: 用户名

        Returns:
            User: 找到的用户，如果不存在或已删除则返回None
        """
        return self.find_one_by(username=username, deleted=0)

    def create_user(self, username: str, name: str, password: str, 
                   telephone: str = None, merchant_code: str = None, creator_id: str = None) -> User:
        """
        创建新用户

        Args:
            username: 用户名
            name: 用户姓名
            password: 用户密码
            telephone: 电话号码（可选）
            merchant_code: 商户代码（可选）
            creator_id: 创建者ID（可选）

        Returns:
            User: 创建的用户

        Note:
            新创建的用户默认角色为"user"
            create_time会自动生成
        """
        # 构建创建参数
        create_params = {
            'username': username,
            'name': name,
            'password': password,
            'role_id': "user"
        }
        
        # 添加可选参数
        if telephone is not None:
            create_params['telephone'] = telephone
        if merchant_code is not None:
            create_params['merchant_code'] = merchant_code
        if creator_id is not None:
            create_params['creator_id'] = creator_id
            
        return self.create(**create_params)

    def get_all_users_with_dict(self) -> List[Dict]:
        """
        获取所有用户（字典格式）

        Returns:
            List[Dict]: 用户字典列表（不包含已删除的用户）
        """
        users = self.find_by(deleted=0)
        return [user.to_dict() for user in users]

    def get_user_dict_by_id(self, user_id: str) -> tuple[Optional[Dict], str]:
        """
        根据ID获取用户字典

        Args:
            user_id: 用户ID（UUID字符串）

        Returns:
            tuple[Optional[Dict], str]: 用户字典和状态("exists", "deleted", "not_found")
        """
        user = self.get_by_id(user_id)
        if not user:
            return None, "not_found"
        elif user.deleted == 1:
            return None, "deleted"
        else:
            return user.to_dict(), "exists"

    def update_user(self, user_id: str, data: Dict) -> Optional[User]:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            data: 更新数据

        Returns:
            User: 更新后的用户，如果不存在则返回None
        """
        user = self.get_by_id(user_id)
        if not user or user.deleted == 1:
            return None
        
        # 过滤掉空值和不存在的字段
        update_data = {}
        allowed_fields = ['username', 'name', 'avatar', 'telephone', 'merchant_code']
        field_mapping = {
            'merchantCode': 'merchant_code'
        }
        
        for key, value in data.items():
            if value is not None and value != '':
                # 处理字段名映射
                db_field = field_mapping.get(key, key)
                if db_field in allowed_fields:
                    update_data[db_field] = value
        
        if update_data:
            return self.update(user, **update_data)
        return user

    def delete_user(self, user_id: str) -> bool:
        """
        删除用户（逻辑删除）

        Args:
            user_id: 用户ID

        Returns:
            bool: 删除是否成功（如果用户不存在或已删除返回False）
        """
        user = self.get_by_id(user_id)
        if not user or user.deleted == 1:
            return False
        
        # 逻辑删除：设置deleted字段为1
        self.update(user, deleted=1)
        return True

    def update_user_status(self, user_id: str, status: int) -> Optional[User]:
        """
        更新用户状态

        Args:
            user_id: 用户ID
            status: 用户状态（1-正常，0-禁用）

        Returns:
            User: 更新后的用户，如果不存在则返回None
        """
        user = self.get_by_id(user_id)
        if not user or user.deleted == 1:
            return None
        
        return self.update(user, status=status)

    def update_user_password(self, user_id: str, password: str) -> Optional[User]:
        """
        更新用户密码

        Args:
            user_id: 用户ID
            password: 新密码

        Returns:
            User: 更新后的用户，如果不存在则返回None
        """
        user = self.get_by_id(user_id)
        if not user or user.deleted == 1:
            return None
        
        return self.update(user, password=password)

    def update_user_role(self, user_id: str, role_id: str) -> Optional[User]:
        """
        更新用户角色

        Args:
            user_id: 用户ID
            role_id: 角色ID

        Returns:
            User: 更新后的用户，如果不存在则返回None
        """
        user = self.get_by_id(user_id)
        if not user or user.deleted == 1:
            return None
        
        return self.update(user, role_id=role_id)
