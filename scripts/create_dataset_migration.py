#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建数据集表的数据库迁移脚本
"""

import os
import subprocess
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_migration():
    """创建数据集表的迁移脚本"""
    print("开始创建数据集表的迁移脚本...")

    # 获取项目根目录
    root_dir = Path(__file__).parent.parent

    # 切换到项目根目录
    os.chdir(root_dir)

    # 创建迁移脚本
    try:
        result = subprocess.run(
            ["flask", "db", "migrate", "-m", "Add dataset table"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("迁移脚本创建成功！")
        print(result.stdout)

        # 获取最新的迁移脚本路径
        migrations_dir = root_dir / "migrations" / "versions"
        migration_files = sorted(migrations_dir.glob("*.py"), key=os.path.getmtime, reverse=True)

        if migration_files:
            latest_migration = migration_files[0]
            print(f"最新的迁移脚本: {latest_migration.name}")
            print("请检查此脚本，确保它只添加了 datasets 表，不会修改现有表")
            print(f"脚本路径: {latest_migration}")

            # 显示迁移脚本内容
            print("\n迁移脚本内容预览:")
            with open(latest_migration, "r") as f:
                content = f.read()
                # 只显示前500个字符
                print(content[:500] + "..." if len(content) > 500 else content)

        print("\n要应用此迁移，请运行:")
        print("flask db upgrade")

    except subprocess.CalledProcessError as e:
        print("创建迁移脚本失败！")
        print(f"错误: {e}")
        print(f"标准输出: {e.stdout}")
        print(f"标准错误: {e.stderr}")
        return False

    return True


if __name__ == "__main__":
    # 设置环境变量
    os.environ["FLASK_APP"] = "wsgi.py"

    # 创建迁移
    create_migration()
