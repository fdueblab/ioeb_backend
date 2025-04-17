"""
字典服务模块
提供字典相关的业务逻辑
"""

import uuid
from typing import List, Dict, Optional

from app.repositories.dictionary_repository import DictionaryRepository


class DictionaryServiceError(Exception):
    """字典服务异常"""
    pass


class DictionaryService:
    """字典服务"""

    def __init__(self):
        """初始化字典服务"""
        self.repository = DictionaryRepository()

    def get_all_dictionaries(self) -> Dict[str, List[Dict]]:
        """
        获取所有字典数据，按类别分组

        Returns:
            Dict[str, List[Dict]]: 按类别分组的字典数据
        """
        all_dictionaries = self.repository.get_all_with_dict()
        result = {}
        
        for dictionary in all_dictionaries:
            category = dictionary['category']
            if category not in result:
                result[category] = []
            result[category].append(dictionary)
            
        return result

    def get_by_category(self, category: str) -> List[Dict]:
        """
        根据类别获取字典列表

        Args:
            category: 字典类别

        Returns:
            List[Dict]: 字典列表
        """
        return self.repository.get_by_category_with_dict(category)

    def get_by_code(self, category: str, code: str) -> Optional[Dict]:
        """
        根据类别和编码获取字典

        Args:
            category: 字典类别
            code: 字典编码

        Returns:
            Optional[Dict]: 字典，如果不存在则返回None
        """
        return self.repository.get_by_code_with_dict(category, code)

    def create(self, category: str, code: str, text: str, sort: int = 0, memo: str = None) -> Dict:
        """
        创建字典

        Args:
            category: 字典类别
            code: 字典编码
            text: 字典文本
            sort: 排序号
            memo: 备注

        Returns:
            Dict: 创建的字典
        """
        # 检查是否已存在
        if self.repository.get_by_code(category, code):
            raise DictionaryServiceError(f"字典已存在: {category}:{code}")

        # 创建字典
        dictionary = self.repository.create(
            id=str(uuid.uuid4()),
            category=category,
            code=code,
            text=text,
            sort=sort,
            memo=memo
        )

        return dictionary.to_dict()

    def update(self, category: str, code: str, **data) -> Dict:
        """
        更新字典

        Args:
            category: 字典类别
            code: 字典编码
            **data: 更新的数据

        Returns:
            Dict: 更新后的字典
        """
        dictionary = self.repository.get_by_code(category, code)
        if not dictionary:
            raise DictionaryServiceError(f"字典不存在: {category}:{code}")

        updated = self.repository.update(dictionary, **data)
        return updated.to_dict()

    def delete(self, category: str, code: str) -> bool:
        """
        删除字典

        Args:
            category: 字典类别
            code: 字典编码

        Returns:
            bool: 删除是否成功
        """
        dictionary = self.repository.get_by_code(category, code)
        if not dictionary:
            raise DictionaryServiceError(f"字典不存在: {category}:{code}")

        return self.repository.delete(dictionary)


# 创建服务实例
dictionary_service = DictionaryService() 