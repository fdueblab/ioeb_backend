"""
腾讯云对象存储工具模块
提供对腾讯云COS的操作封装
"""

import logging
import os
import uuid
from typing import BinaryIO, Dict, List, Tuple

from qcloud_cos import CosConfig, CosS3Client


class COSError(Exception):
    """COS操作错误"""


class COSUtils:
    """腾讯云对象存储工具类"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(COSUtils, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化COS工具类"""
        if self._initialized:
            return

        self._client = None
        self._bucket = None
        self._region = None
        self._initialized = True

    def init_app(self, app):
        """使用应用配置初始化COS客户端

        Args:
            app: Flask应用实例
        """
        self._region = app.config.get("COS_REGION")
        self._bucket = app.config.get("COS_BUCKET")

        # 获取密钥
        secret_id = app.config.get("COS_SECRET_ID") or os.environ.get("COS_SECRET_ID")
        secret_key = app.config.get("COS_SECRET_KEY") or os.environ.get("COS_SECRET_KEY")

        if not secret_id or not secret_key:
            app.logger.warning("COS credentials not configured. COS operations will not work.")
            return

        if not self._region or not self._bucket:
            app.logger.warning("COS region or bucket not configured. COS operations will not work.")
            return

        # 创建COS配置
        config = CosConfig(
            Region=self._region, SecretId=secret_id, SecretKey=secret_key, Scheme="https"
        )

        # 创建COS客户端
        self._client = CosS3Client(config)
        app.logger.info(
            f"COS client initialized with region: {self._region}, bucket: {self._bucket}"
        )

    @property
    def client(self) -> CosS3Client:
        """获取COS客户端

        Returns:
            CosS3Client: COS客户端实例

        Raises:
            COSError: 如果客户端未初始化
        """
        if not self._client:
            raise COSError("COS client not initialized")
        return self._client

    @property
    def bucket(self) -> str:
        """获取存储桶名称

        Returns:
            str: 存储桶名称

        Raises:
            COSError: 如果存储桶未配置
        """
        if not self._bucket:
            raise COSError("COS bucket not configured")
        return self._bucket

    def upload_file(self, local_path: str, cos_path: str, metadata: Dict = None) -> Dict:
        """上传文件到COS

        Args:
            local_path: 本地文件路径
            cos_path: COS对象键（路径）
            metadata: 对象元数据

        Returns:
            Dict: 上传结果，包含ETag等信息

        Raises:
            COSError: 上传失败时抛出
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(local_path):
                raise COSError(f"File not found: {local_path}")

            # 上传文件
            response = self.client.upload_file(
                Bucket=self.bucket,
                LocalFilePath=local_path,
                Key=cos_path,
                Metadata=metadata,
                PartSize=1,  # 分块上传时的分块大小，单位为MB
                MAXThread=10,  # 分块上传时的最大线程数
            )

            return response
        except Exception as e:
            logging.error(f"Failed to upload file to COS: {str(e)}")
            raise COSError(f"Failed to upload file to COS: {str(e)}")

    def upload_file_from_bytes(
        self, file_bytes: bytes, cos_path: str, metadata: Dict = None
    ) -> Dict:
        """从字节数据上传文件到COS

        Args:
            file_bytes: 文件字节数据
            cos_path: COS对象键（路径）
            metadata: 对象元数据

        Returns:
            Dict: 上传结果，包含ETag等信息

        Raises:
            COSError: 上传失败时抛出
        """
        try:
            # 上传文件
            response = self.client.put_object(
                Bucket=self.bucket, Body=file_bytes, Key=cos_path, Metadata=metadata
            )

            return response
        except Exception as e:
            logging.error(f"Failed to upload bytes to COS: {str(e)}")
            raise COSError(f"Failed to upload bytes to COS: {str(e)}")

    def upload_file_from_stream(
        self, file_stream: BinaryIO, cos_path: str, metadata: Dict = None
    ) -> Dict:
        """从文件流上传文件到COS

        Args:
            file_stream: 文件流对象
            cos_path: COS对象键（路径）
            metadata: 对象元数据

        Returns:
            Dict: 上传结果，包含ETag等信息

        Raises:
            COSError: 上传失败时抛出
        """
        try:
            # 上传文件
            response = self.client.put_object(
                Bucket=self.bucket, Body=file_stream, Key=cos_path, Metadata=metadata
            )

            return response
        except Exception as e:
            logging.error(f"Failed to upload stream to COS: {str(e)}")
            raise COSError(f"Failed to upload stream to COS: {str(e)}")

    def download_file(self, cos_path: str, local_path: str) -> bool:
        """从COS下载文件

        Args:
            cos_path: COS对象键（路径）
            local_path: 本地保存路径

        Returns:
            bool: 下载是否成功

        Raises:
            COSError: 下载失败时抛出
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)

            # 下载文件
            response = self.client.get_object(Bucket=self.bucket, Key=cos_path)

            # 保存到本地
            response["Body"].get_stream_to_file(local_path)

            return True
        except Exception as e:
            logging.error(f"Failed to download file from COS: {str(e)}")
            raise COSError(f"Failed to download file from COS: {str(e)}")

    def get_file_url(self, cos_path: str, expired: int = 3600) -> str:
        """获取文件的临时访问URL

        Args:
            cos_path: COS对象键（路径）
            expired: 链接有效期，单位为秒，默认1小时

        Returns:
            str: 预签名URL

        Raises:
            COSError: 获取URL失败时抛出
        """
        try:
            # 生成预签名URL
            url = self.client.get_presigned_url(
                Method="GET", Bucket=self.bucket, Key=cos_path, Expired=expired
            )

            return url
        except Exception as e:
            logging.error(f"Failed to get file URL from COS: {str(e)}")
            raise COSError(f"Failed to get file URL from COS: {str(e)}")

    def delete_file(self, cos_path: str) -> bool:
        """删除COS上的文件

        Args:
            cos_path: COS对象键（路径）

        Returns:
            bool: 删除是否成功

        Raises:
            COSError: 删除失败时抛出
        """
        try:
            # 删除文件
            self.client.delete_object(Bucket=self.bucket, Key=cos_path)

            return True
        except Exception as e:
            logging.error(f"Failed to delete file from COS: {str(e)}")
            raise COSError(f"Failed to delete file from COS: {str(e)}")

    def delete_files(self, cos_paths: List[str]) -> Tuple[List[str], List[str]]:
        """批量删除COS上的文件

        Args:
            cos_paths: COS对象键（路径）列表

        Returns:
            Tuple[List[str], List[str]]: 成功删除的文件列表和失败的文件列表

        Raises:
            COSError: 删除失败时抛出
        """
        try:
            # 批量删除文件
            response = self.client.delete_objects(
                Bucket=self.bucket,
                Delete={"Object": [{"Key": path} for path in cos_paths], "Quiet": "false"},
            )

            # 处理结果
            deleted = [item.get("Key") for item in response.get("Deleted", [])]
            errors = [item.get("Key") for item in response.get("Error", [])]

            return deleted, errors
        except Exception as e:
            logging.error(f"Failed to batch delete files from COS: {str(e)}")
            raise COSError(f"Failed to batch delete files from COS: {str(e)}")

    def check_file_exists(self, cos_path: str) -> bool:
        """检查COS上的文件是否存在

        Args:
            cos_path: COS对象键（路径）

        Returns:
            bool: 文件是否存在
        """
        try:
            # 检查文件是否存在
            self.client.head_object(Bucket=self.bucket, Key=cos_path)
            return True
        except Exception:
            return False

    def list_files(self, prefix: str = "", delimiter: str = "", max_keys: int = 1000) -> Dict:
        """列出COS上的文件

        Args:
            prefix: 前缀
            delimiter: 分隔符
            max_keys: 最大返回数量

        Returns:
            Dict: 文件列表信息

        Raises:
            COSError: 列出文件失败时抛出
        """
        try:
            # 列出文件
            response = self.client.list_objects(
                Bucket=self.bucket, Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys
            )

            return response
        except Exception as e:
            logging.error(f"Failed to list files from COS: {str(e)}")
            raise COSError(f"Failed to list files from COS: {str(e)}")

    def generate_cos_path(self, filename: str, prefix: str = "") -> str:
        """生成COS对象键（路径）

        Args:
            filename: 文件名
            prefix: 前缀目录

        Returns:
            str: COS对象键
        """
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"

        # 构建路径
        if prefix:
            # 确保前缀以/结尾
            if not prefix.endswith("/"):
                prefix = f"{prefix}/"
            return f"{prefix}{unique_filename}"
        else:
            return unique_filename


# 创建单例实例
cos_utils = COSUtils()
