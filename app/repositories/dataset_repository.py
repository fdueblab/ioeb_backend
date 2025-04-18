"""
数据集数据仓库模块
提供对数据集数据模型的基础操作接口
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from app.extensions import db
from app.models.dataset import Dataset
from app.repositories.base_repository import BaseRepository


class DatasetRepository(BaseRepository[Dataset]):
    """数据集数据仓库"""

    def __init__(self):
        """初始化数据集数据仓库"""
        super().__init__(Dataset)

    def get_all_datasets(self, include_deleted: bool = False) -> List[Dataset]:
        """
        获取所有数据集

        Args:
            include_deleted: 是否包含已删除的数据集

        Returns:
            List[Dataset]: 数据集对象列表
        """
        if include_deleted:
            return Dataset.query.all()
        else:
            return Dataset.query.filter(Dataset.status != "deleted").all()

    def get_all_datasets_with_dict(self, include_deleted: bool = False) -> List[Dict]:
        """
        获取所有数据集的字典表示

        Args:
            include_deleted: 是否包含已删除的数据集

        Returns:
            List[Dict]: 数据集字典列表
        """
        datasets = self.get_all_datasets(include_deleted)
        return [dataset.to_dict() for dataset in datasets]

    def get_dataset_by_id(self, dataset_id: str) -> Optional[Dataset]:
        """
        根据ID获取数据集

        Args:
            dataset_id: 数据集ID

        Returns:
            Optional[Dataset]: 数据集对象，如果不存在则返回None
        """
        return Dataset.query.filter_by(id=dataset_id).first()

    def get_dataset_dict_by_id(self, dataset_id: str) -> Optional[Dict]:
        """
        根据ID获取数据集的字典表示

        Args:
            dataset_id: 数据集ID

        Returns:
            Optional[Dict]: 数据集字典，如果不存在则返回None
        """
        dataset = self.get_dataset_by_id(dataset_id)
        return dataset.to_dict() if dataset else None

    def find_by_name(self, name: str, exact_match: bool = True) -> List[Dataset]:
        """
        根据名称查找数据集

        Args:
            name: 数据集名称
            exact_match: 是否精确匹配，如果为False则使用模糊匹配

        Returns:
            List[Dataset]: 数据集对象列表
        """
        if exact_match:
            return Dataset.query.filter_by(name=name, status="active").all()
        else:
            return Dataset.query.filter(
                Dataset.name.like(f"%{name}%"), Dataset.status == "active"
            ).all()

    def search_by_keyword(self, keyword: str) -> List[Dataset]:
        """
        根据关键词搜索数据集

        Args:
            keyword: 搜索关键词，匹配数据集名称或描述

        Returns:
            List[Dataset]: 符合条件的数据集对象列表
        """
        return Dataset.query.filter(
            db.or_(Dataset.name.like(f"%{keyword}%"), Dataset.description.like(f"%{keyword}%")),
            Dataset.status == "active",
        ).all()

    def create_dataset(self, dataset_data: Dict) -> Dataset:
        """
        创建新数据集

        Args:
            dataset_data: 包含数据集信息的字典

        Returns:
            Dataset: 创建的数据集对象
        """
        # 确保有ID和时间戳
        if "id" not in dataset_data:
            dataset_data["id"] = str(uuid.uuid4())

        current_time = int(datetime.now().timestamp())
        if "create_time" not in dataset_data:
            dataset_data["create_time"] = current_time
        if "update_time" not in dataset_data:
            dataset_data["update_time"] = current_time

        # 创建数据集
        dataset = Dataset(**dataset_data)
        db.session.add(dataset)
        db.session.commit()
        return dataset

    def update_dataset(self, dataset_id: str, dataset_data: Dict) -> Optional[Dataset]:
        """
        更新数据集信息

        Args:
            dataset_id: 数据集ID
            dataset_data: 更新的数据集数据

        Returns:
            Optional[Dataset]: 更新后的数据集对象，如果不存在则返回None
        """
        dataset = self.get_dataset_by_id(dataset_id)
        if not dataset:
            return None

        # 更新时间戳
        dataset_data["update_time"] = int(datetime.now().timestamp())

        # 更新数据集
        for key, value in dataset_data.items():
            if hasattr(dataset, key):
                setattr(dataset, key, value)

        db.session.commit()
        return dataset

    def delete_dataset(self, dataset_id: str, hard_delete: bool = False) -> bool:
        """
        删除数据集

        Args:
            dataset_id: 数据集ID
            hard_delete: 是否硬删除，如果为False则软删除（更新状态为deleted）

        Returns:
            bool: 是否删除成功
        """
        dataset = self.get_dataset_by_id(dataset_id)
        if not dataset:
            return False

        if hard_delete:
            # 硬删除
            db.session.delete(dataset)
        else:
            # 软删除
            dataset.status = "deleted"
            dataset.update_time = int(datetime.now().timestamp())

        db.session.commit()
        return True

    def filter_datasets(self, **filters) -> List[Dataset]:
        """
        根据条件筛选数据集

        Args:
            **filters: 筛选条件，可包括:
                - status: 状态
                - file_type: 文件类型
                - file_extension: 文件扩展名
                - tags: 标签

        Returns:
            List[Dataset]: 符合条件的数据集对象列表
        """
        query = Dataset.query

        # 应用筛选条件
        for key, value in filters.items():
            if key == "status" and value is not None:
                query = query.filter(Dataset.status == value)
            elif key == "file_type" and value is not None:
                query = query.filter(Dataset.file_type == value)
            elif key == "file_extension" and value is not None:
                query = query.filter(Dataset.file_extension == value)
            elif key == "tags" and value is not None:
                # 标签筛选需要特殊处理，这里简化处理
                # 实际实现可能需要根据数据库类型进行调整
                if isinstance(value, list):
                    for tag in value:
                        query = query.filter(Dataset.tags.contains(tag))
                else:
                    query = query.filter(Dataset.tags.contains(value))

        return query.all()
