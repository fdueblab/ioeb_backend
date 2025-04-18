"""
数据集服务模块
处理数据集相关的业务逻辑
"""

import os
from typing import Dict, List

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage

from app.repositories.dataset_repository import DatasetRepository
from app.utils.cos_utils import COSError, cos_utils


class DatasetServiceError(Exception):
    """数据集服务错误"""


class DatasetService:
    """数据集服务类"""

    def __init__(self):
        """初始化数据集服务"""
        self.dataset_repository = DatasetRepository()

    def get_all_datasets(self, include_deleted: bool = False) -> List[Dict]:
        """
        获取所有数据集

        Args:
            include_deleted: 是否包含已删除的数据集

        Returns:
            List[Dict]: 数据集列表，每个数据集以字典形式表示
        """
        try:
            return self.dataset_repository.get_all_datasets_with_dict(include_deleted)
        except Exception as e:
            raise DatasetServiceError(f"获取数据集列表失败: {str(e)}")

    def get_dataset_by_id(self, dataset_id: str) -> Dict:
        """
        根据ID获取数据集

        Args:
            dataset_id: 数据集ID

        Returns:
            Dict: 数据集信息字典

        Raises:
            DatasetServiceError: 数据集不存在时抛出
        """
        try:
            dataset_dict = self.dataset_repository.get_dataset_dict_by_id(dataset_id)
            if not dataset_dict:
                raise DatasetServiceError(f"数据集ID {dataset_id} 不存在")
            return dataset_dict
        except Exception as e:
            if isinstance(e, DatasetServiceError):
                raise
            raise DatasetServiceError(f"获取数据集失败: {str(e)}")

    def search_datasets(self, keyword: str) -> List[Dict]:
        """
        搜索数据集

        Args:
            keyword: 搜索关键词，匹配数据集名称或描述

        Returns:
            List[Dict]: 符合条件的数据集列表
        """
        try:
            datasets = self.dataset_repository.search_by_keyword(keyword)
            return [dataset.to_dict() for dataset in datasets]
        except Exception as e:
            raise DatasetServiceError(f"搜索数据集失败: {str(e)}")

    def filter_datasets(self, **filters) -> List[Dict]:
        """
        根据条件筛选数据集

        Args:
            **filters: 筛选条件，可包括:
                - status: 状态
                - file_type: 文件类型
                - file_extension: 文件扩展名
                - tags: 标签

        Returns:
            List[Dict]: 符合条件的数据集列表
        """
        try:
            datasets = self.dataset_repository.filter_datasets(**filters)
            return [dataset.to_dict() for dataset in datasets]
        except Exception as e:
            raise DatasetServiceError(f"筛选数据集失败: {str(e)}")

    def create_dataset_from_file(  # noqa: C901
        self,
        file: FileStorage,
        name: str,
        description: str = None,
        tags: List[str] = None,
        metadata: Dict = None,
        creator_id: str = None,
    ) -> Dict:
        """
        从上传文件创建数据集

        Args:
            file: 上传的文件对象
            name: 数据集名称
            description: 数据集描述
            tags: 标签列表
            metadata: 元数据
            creator_id: 创建者ID

        Returns:
            Dict: 创建的数据集信息

        Raises:
            DatasetServiceError: 创建过程中出错
        """
        if not file or not name:
            raise DatasetServiceError("文件和数据集名称不能为空")

        try:
            # 获取文件信息
            filename = file.filename
            file_size = 0
            file_extension = os.path.splitext(filename)[1].lower().lstrip(".")

            # 确定文件类型
            file_type = self._determine_file_type(file_extension)

            # 生成COS路径
            cos_prefix = f"datasets/{file_type}"
            cos_path = cos_utils.generate_cos_path(filename, cos_prefix)

            # 上传文件到COS
            try:
                # 获取文件大小
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)

                # 上传文件
                cos_utils.upload_file_from_stream(file, cos_path)
            except COSError as e:
                raise DatasetServiceError(f"上传文件到COS失败: {str(e)}")

            # 创建数据集记录
            dataset_data = {
                "name": name,
                "description": description,
                "file_key": cos_path,
                "file_name": filename,
                "file_size": file_size,
                "file_type": file_type,
                "file_extension": file_extension,
                "meta_data": metadata or {},
                "tags": tags or [],
                "status": "active",
                "creator_id": creator_id,
            }

            dataset = self.dataset_repository.create_dataset(dataset_data)
            return dataset.to_dict()
        except SQLAlchemyError as e:
            # 如果数据库操作失败，尝试删除已上传的文件
            try:
                if cos_path:
                    cos_utils.delete_file(cos_path)
            except Exception:
                pass
            raise DatasetServiceError(f"创建数据集失败: {str(e)}")
        except Exception as e:
            # 如果其他操作失败，尝试删除已上传的文件
            try:
                if cos_path:
                    cos_utils.delete_file(cos_path)
            except Exception:
                pass
            raise DatasetServiceError(f"创建数据集过程中出错: {str(e)}")

    def create_dataset_from_local_file(  # noqa: C901
        self,
        file_path: str,
        name: str,
        description: str = None,
        tags: List[str] = None,
        metadata: Dict = None,
        creator_id: str = None,
    ) -> Dict:
        """
        从本地文件创建数据集

        Args:
            file_path: 本地文件路径
            name: 数据集名称
            description: 数据集描述
            tags: 标签列表
            metadata: 元数据
            creator_id: 创建者ID

        Returns:
            Dict: 创建的数据集信息

        Raises:
            DatasetServiceError: 创建过程中出错
        """
        if not file_path or not name:
            raise DatasetServiceError("文件路径和数据集名称不能为空")

        if not os.path.exists(file_path):
            raise DatasetServiceError(f"文件不存在: {file_path}")

        try:
            # 获取文件信息
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(filename)[1].lower().lstrip(".")

            # 确定文件类型
            file_type = self._determine_file_type(file_extension)

            # 生成COS路径
            cos_prefix = f"datasets/{file_type}"
            cos_path = cos_utils.generate_cos_path(filename, cos_prefix)

            # 上传文件到COS
            try:
                cos_utils.upload_file(file_path, cos_path)
            except COSError as e:
                raise DatasetServiceError(f"上传文件到COS失败: {str(e)}")

            # 创建数据集记录
            dataset_data = {
                "name": name,
                "description": description,
                "file_key": cos_path,
                "file_name": filename,
                "file_size": file_size,
                "file_type": file_type,
                "file_extension": file_extension,
                "meta_data": metadata or {},
                "tags": tags or [],
                "status": "active",
                "creator_id": creator_id,
            }

            dataset = self.dataset_repository.create_dataset(dataset_data)
            return dataset.to_dict()
        except SQLAlchemyError as e:
            # 如果数据库操作失败，尝试删除已上传的文件
            try:
                if cos_path:
                    cos_utils.delete_file(cos_path)
            except Exception:
                pass
            raise DatasetServiceError(f"创建数据集失败: {str(e)}")
        except Exception as e:
            # 如果其他操作失败，尝试删除已上传的文件
            try:
                if cos_path:
                    cos_utils.delete_file(cos_path)
            except Exception:
                pass
            raise DatasetServiceError(f"创建数据集过程中出错: {str(e)}")

    def update_dataset(self, dataset_id: str, dataset_data: Dict) -> Dict:
        """
        更新数据集信息

        Args:
            dataset_id: 数据集ID
            dataset_data: 更新的数据集数据，可包括:
                - name: 数据集名称
                - description: 数据集描述
                - tags: 标签列表
                - metadata: 元数据
                - status: 状态

        Returns:
            Dict: 更新后的数据集信息

        Raises:
            DatasetServiceError: 更新过程中出错
        """
        try:
            # 检查数据集是否存在
            dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
            if not dataset:
                raise DatasetServiceError(f"数据集ID {dataset_id} 不存在")

            # 过滤可更新的字段
            allowed_fields = ["name", "description", "tags", "status"]
            update_data = {k: v for k, v in dataset_data.items() if k in allowed_fields}

            # 如果有metadata字段，将其映射到meta_data字段
            if "metadata" in dataset_data:
                update_data["meta_data"] = dataset_data["metadata"]

            # 更新数据集
            updated_dataset = self.dataset_repository.update_dataset(dataset_id, update_data)
            return updated_dataset.to_dict()
        except SQLAlchemyError as e:
            raise DatasetServiceError(f"更新数据集失败: {str(e)}")
        except Exception as e:
            if isinstance(e, DatasetServiceError):
                raise
            raise DatasetServiceError(f"更新数据集过程中出错: {str(e)}")

    def delete_dataset(self, dataset_id: str, delete_file: bool = True) -> bool:
        """
        删除数据集

        Args:
            dataset_id: 数据集ID
            delete_file: 是否同时删除COS上的文件

        Returns:
            bool: 删除是否成功

        Raises:
            DatasetServiceError: 删除过程中出错
        """
        try:
            # 检查数据集是否存在
            dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
            if not dataset:
                raise DatasetServiceError(f"数据集ID {dataset_id} 不存在")

            # 如果需要删除文件，先获取文件路径
            file_key = dataset.file_key if delete_file else None

            # 删除数据集记录（软删除）
            success = self.dataset_repository.delete_dataset(dataset_id, hard_delete=False)
            if not success:
                raise DatasetServiceError("删除数据集记录失败")

            # 如果需要删除文件，删除COS上的文件
            if file_key and delete_file:
                try:
                    cos_utils.delete_file(file_key)
                except COSError as e:
                    current_app.logger.warning(f"删除COS文件失败: {str(e)}")
                    # 不影响整体删除结果

            return True
        except Exception as e:
            if isinstance(e, DatasetServiceError):
                raise
            raise DatasetServiceError("删除数据集过程中出错: {}".format(str(e)))

    def get_dataset_download_url(self, dataset_id: str, expired: int = 3600) -> str:
        """
        获取数据集文件的下载URL

        Args:
            dataset_id: 数据集ID
            expired: URL有效期，单位为秒，默认1小时

        Returns:
            str: 下载URL

        Raises:
            DatasetServiceError: 获取URL过程中出错
        """
        try:
            # 检查数据集是否存在
            dataset = self.dataset_repository.get_dataset_by_id(dataset_id)
            if not dataset:
                raise DatasetServiceError(f"数据集ID {dataset_id} 不存在")

            # 检查数据集状态
            if dataset.status == "deleted":
                raise DatasetServiceError("数据集已删除")

            # 获取文件路径
            file_key = dataset.file_key
            if not file_key:
                raise DatasetServiceError("数据集文件路径为空")

            # 获取下载URL
            try:
                url = cos_utils.get_file_url(file_key, expired)
                return url
            except COSError as e:
                raise DatasetServiceError("获取下载URL失败: {}".format(str(e)))
        except Exception as e:
            if isinstance(e, DatasetServiceError):
                raise
            raise DatasetServiceError("获取数据集下载URL过程中出错: {}".format(str(e)))

    def _determine_file_type(self, file_extension: str) -> str:
        """
        根据文件扩展名确定文件类型

        Args:
            file_extension: 文件扩展名

        Returns:
            str: 文件类型
        """
        # 图片类型
        image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
        # 音频类型
        audio_extensions = ["mp3", "wav", "ogg", "flac", "aac", "m4a"]
        # 视频类型
        video_extensions = ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]
        # 文档类型
        document_extensions = [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "txt",
            "csv",
            "json",
            "xml",
        ]
        # 压缩文件类型
        archive_extensions = ["zip", "rar", "7z", "tar", "gz"]

        file_extension = file_extension.lower()

        if file_extension in image_extensions:
            return "image"
        elif file_extension in audio_extensions:
            return "audio"
        elif file_extension in video_extensions:
            return "video"
        elif file_extension in document_extensions:
            return "document"
        elif file_extension in archive_extensions:
            return "archive"
        else:
            return "other"


# 创建单例实例
dataset_service = DatasetService()
