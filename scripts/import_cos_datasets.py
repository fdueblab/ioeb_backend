#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导入腾讯云对象存储中的数据集文件到数据库
"""

import argparse
import datetime
import os
import sys
import uuid
from pathlib import Path

from sqlalchemy import inspect

from app import create_app
from app.extensions import db
from app.models.dataset import Dataset
from app.utils.cos_utils import COSError, cos_utils
from app.utils.flask_utils import get_flask_env

# 将项目根目录添加到 Python 路径
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="导入腾讯云对象存储中的数据集文件到数据库")
    parser.add_argument("--prefix", type=str, default="datasets/", help="COS对象前缀路径")
    parser.add_argument("--creator-id", type=str, help="创建者ID")
    parser.add_argument("--dry-run", action="store_true", help="仅打印不执行导入")
    parser.add_argument("--force", action="store_true", help="强制导入，即使文件已存在于数据库中")
    return parser.parse_args()


def determine_file_type(file_extension):
    """根据文件扩展名确定文件类型"""
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


def get_existing_file_keys():
    """获取数据库中已存在的文件键列表"""
    return [dataset.file_key for dataset in Dataset.query.all()]


def check_dataset_table_exists():
    """检查数据集表是否存在"""

    inspector = inspect(db.engine)
    if "datasets" not in inspector.get_table_names():
        print("错误: 数据集表不存在，请先运行 'flask db upgrade' 创建表")
        return False
    return True


def create_dataset_record(file, creator_id):
    """根据文件信息创建数据集记录数据"""
    file_key = file["Key"]
    file_size = file["Size"]
    file_name = Path(file_key).name
    file_extension = Path(file_key).suffix.lstrip(".").lower()
    file_type = determine_file_type(file_extension)

    # 生成数据集名称
    dataset_name = f"{file_type.capitalize()} - {file_name}"

    # 创建数据集记录
    return {
        "id": str(uuid.uuid4()),
        "name": dataset_name,
        "description": f"从COS导入的{file_type}文件",
        "file_key": file_key,
        "file_name": file_name,
        "file_size": file_size,
        "file_type": file_type,
        "file_extension": file_extension,
        "meta_data": {},
        "tags": [file_type],
        "status": "active",
        "create_time": int(datetime.datetime.now().timestamp() * 1000), # 毫秒时间戳
        "update_time": int(datetime.datetime.now().timestamp() * 1000), # 毫秒时间戳
        "creator_id": creator_id,
    }


def process_file(file, existing_file_keys, creator_id, dry_run=False):
    """处理单个文件"""
    file_key = file["Key"]

    # 跳过目录
    if file_key.endswith("/"):
        return None, None

    # 检查是否已存在
    if file_key in existing_file_keys:
        print(f"跳过已存在的文件: {file_key}")
        return None, "skipped"

    try:
        # 创建数据集记录数据
        dataset_data = create_dataset_record(file, creator_id)

        if dry_run:
            print(f"[DRY RUN] 将导入文件: {file_key}")
            return None, "imported"

        # 创建数据集记录
        dataset = Dataset(**dataset_data)
        db.session.add(dataset)
        db.session.commit()

        print(f"成功导入文件: {file_key}")
        return None, "imported"

    except Exception as e:
        print(f"导入文件 {file_key} 失败: {e}")
        db.session.rollback()
        return None, "error"


def process_files_batch(files, existing_file_keys, creator_id, dry_run=False):
    """处理一批文件"""
    imported_count = 0
    skipped_count = 0
    error_count = 0

    for file in files:
        _, result = process_file(file, existing_file_keys, creator_id, dry_run)
        if result == "imported":
            imported_count += 1
        elif result == "skipped":
            skipped_count += 1
        elif result == "error":
            error_count += 1

    return imported_count, skipped_count, error_count


def import_cos_files(prefix, creator_id, dry_run=False, force=False):
    """导入COS文件到数据库"""
    print(f"开始导入COS文件，前缀: {prefix}")

    # 检查数据集表是否存在
    if not check_dataset_table_exists():
        return

    # 获取已存在的文件键
    existing_file_keys = [] if force else get_existing_file_keys()
    print(f"数据库中已存在 {len(existing_file_keys)} 个文件记录")

    # 导入统计
    total_imported = 0
    total_skipped = 0
    total_error = 0

    # 列出COS中的文件
    try:
        response = cos_utils.list_files(prefix=prefix, max_keys=1000)
    except COSError as e:
        print(f"列出COS文件失败: {e}")
        return

    if "Contents" not in response:
        print("未找到文件")
        return

    files = response["Contents"]
    print(f"找到 {len(files)} 个文件")

    # 处理第一批文件
    imported, skipped, error = process_files_batch(files, existing_file_keys, creator_id, dry_run)
    total_imported += imported
    total_skipped += skipped
    total_error += error

    # 处理分页
    while response.get("IsTruncated") == "true":
        marker = response.get("NextMarker")
        try:
            response = cos_utils.list_files(prefix=prefix, marker=marker, max_keys=1000)

            if "Contents" not in response:
                break

            files = response["Contents"]
            print(f"找到额外的 {len(files)} 个文件")

            # 处理下一批文件
            imported, skipped, error = process_files_batch(
                files, existing_file_keys, creator_id, dry_run
            )
            total_imported += imported
            total_skipped += skipped
            total_error += error

        except COSError as e:
            print(f"列出更多COS文件失败: {e}")
            break

    print("\n导入统计:")
    print(f"总文件数: {total_imported + total_skipped + total_error}")
    print(f"成功导入: {total_imported}")
    print(f"已跳过: {total_skipped}")
    print(f"导入失败: {total_error}")


def main():
    """主函数"""
    args = parse_args()

    # 创建应用上下文
    env = get_flask_env()
    app = create_app(env)

    with app.app_context():
        # 检查COS工具是否初始化
        if not hasattr(cos_utils, "_client") or cos_utils._client is None:
            print("COS工具未正确初始化，请检查环境变量或配置")
            return

        # 导入文件
        import_cos_files(
            prefix=args.prefix, creator_id=args.creator_id, dry_run=args.dry_run, force=args.force
        )


if __name__ == "__main__":
    main()
