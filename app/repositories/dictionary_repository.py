"""
字典数据仓库模块
提供对字典数据模型的基础操作接口
"""

from typing import List, Optional, Dict

from app.repositories.base_repository import BaseRepository
from app.models.dictionary import Dictionary


class DictionaryRepository(BaseRepository[Dictionary]):
    """字典数据仓库"""

    def __init__(self):
        """初始化字典数据仓库"""
        super().__init__(Dictionary)

    def get_by_category(self, category: str) -> List[Dictionary]:
        """
        根据类别获取字典列表

        Args:
            category: 字典类别

        Returns:
            List[Dictionary]: 字典对象列表
        """
        return self.model_class.query.filter_by(category=category).order_by(Dictionary.sort).all()

    def get_by_category_with_dict(self, category: str) -> List[Dict]:
        """
        根据类别获取字典列表的字典表示

        Args:
            category: 字典类别

        Returns:
            List[Dict]: 字典列表
        """
        dictionaries = self.get_by_category(category)
        return [dictionary.to_dict() for dictionary in dictionaries]

    def get_by_code(self, category: str, code: str) -> Optional[Dictionary]:
        """
        根据类别和编码获取字典

        Args:
            category: 字典类别
            code: 字典编码

        Returns:
            Optional[Dictionary]: 字典对象，如果不存在则返回None
        """
        return self.model_class.query.filter_by(category=category, code=code).first()

    def get_by_code_with_dict(self, category: str, code: str) -> Optional[Dict]:
        """
        根据类别和编码获取字典的字典表示

        Args:
            category: 字典类别
            code: 字典编码

        Returns:
            Optional[Dict]: 字典，如果不存在则返回None
        """
        dictionary = self.get_by_code(category, code)
        return dictionary.to_dict() if dictionary else None 