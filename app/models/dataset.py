"""
数据集数据模型
定义与datasets数据库表结构
"""

import datetime
import uuid

from app.extensions import db


class Dataset(db.Model):
    """Dataset模型"""

    __tablename__ = "datasets"

    # 主键和基本信息
    id = db.Column(db.String(36), primary_key=True, comment="数据集ID")
    name = db.Column(db.String(100), nullable=False, comment="数据集名称")
    description = db.Column(db.Text, nullable=True, comment="数据集描述")

    # 文件信息
    file_key = db.Column(db.String(255), nullable=False, comment="COS对象键")
    file_name = db.Column(db.String(255), nullable=False, comment="原始文件名")
    file_size = db.Column(db.BigInteger, nullable=False, comment="文件大小(字节)")
    file_type = db.Column(db.String(50), nullable=False, comment="文件类型")
    file_extension = db.Column(db.String(20), nullable=False, comment="文件扩展名")

    # 元数据
    meta_data = db.Column(db.JSON, nullable=True, comment="元数据")
    tags = db.Column(db.JSON, nullable=True, comment="标签")

    # 状态信息
    status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
        comment="状态：active-可用，archived-已归档，deleted-已删除",
    )

    # 创建和更新信息
    create_time = db.Column(db.BigInteger, nullable=False, comment="创建时间戳")
    update_time = db.Column(db.BigInteger, nullable=False, comment="更新时间戳")
    creator_id = db.Column(db.String(36), nullable=True, comment="创建者ID")

    def __init__(self, **kwargs):
        """初始化数据集实例"""
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        current_time = int(datetime.datetime.now().timestamp() * 1000) # 毫秒时间戳
        if not self.create_time:
            self.create_time = current_time
        if not self.update_time:
            self.update_time = current_time

    def __repr__(self):
        return f"<Dataset {self.name}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "fileKey": self.file_key,
            "fileName": self.file_name,
            "fileSize": self.file_size,
            "fileType": self.file_type,
            "fileExtension": self.file_extension,
            "metadata": self.meta_data,
            "tags": self.tags,
            "status": self.status,
            "createTime": self.create_time,
            "updateTime": self.update_time,
            "creatorId": self.creator_id,
        }
