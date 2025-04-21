#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用数据集表的数据库迁移
"""

import os
import subprocess
import sys
from pathlib import Path

from sqlalchemy import inspect

from app import create_app
from app.extensions import db
from app.utils.flask_utils import get_flask_env

# 将项目根目录添加到 Python 路径
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


def apply_migration():
    """应用数据库迁移"""
    print("开始应用数据库迁移...")

    # 获取项目根目录
    root_dir = Path(__file__).parent.parent

    # 切换到项目根目录
    os.chdir(root_dir)

    # 应用迁移
    try:
        result = subprocess.run(
            ["flask", "db", "upgrade"], capture_output=True, text=True, check=True
        )
        print("迁移应用成功！")
        print(result.stdout)

        # 检查数据集表是否已创建
        env = get_flask_env()
        app = create_app(env)

        with app.app_context():

            inspector = inspect(db.engine)
            if "datasets" in inspector.get_table_names():
                print("数据集表已成功创建！")

                # 显示表结构
                columns = inspector.get_columns("datasets")
                print("\n数据集表结构:")
                for column in columns:
                    print(f"- {column['name']}: {column['type']}")
            else:
                print("警告: 数据集表未创建，请检查迁移脚本")

    except subprocess.CalledProcessError as e:
        print("应用迁移失败！")
        print(f"错误: {e}")
        print(f"标准输出: {e.stdout}")
        print(f"标准错误: {e.stderr}")
        return False

    return True


if __name__ == "__main__":
    # 设置环境变量
    os.environ["FLASK_APP"] = "wsgi.py"

    # 应用迁移
    apply_migration()
