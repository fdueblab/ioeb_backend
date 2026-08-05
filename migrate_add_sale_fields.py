"""
数据库迁移脚本：添加销售相关字段和表
使用Flask应用上下文执行迁移
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from sqlalchemy import text

def migrate():
    """执行数据库迁移"""
    app = create_app('development')

    with app.app_context():
        print("开始数据库迁移...")

        # 1. 为services表添加销售相关字段
        print("1. 为services表添加销售相关字段...")

        # 检查数据库类型
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        is_mysql = 'mysql' in db_uri

        if is_mysql:
            # MySQL语法
            alter_statements = [
                "ALTER TABLE services ADD COLUMN is_for_sale BOOLEAN DEFAULT 0",
                "ALTER TABLE services ADD COLUMN sale_price FLOAT DEFAULT 0.0",
                "ALTER TABLE services ADD COLUMN sale_description TEXT",
                "ALTER TABLE services ADD COLUMN sale_status VARCHAR(20) DEFAULT 'unpublished'",
            ]
        else:
            # SQLite语法
            alter_statements = [
                "ALTER TABLE services ADD COLUMN is_for_sale BOOLEAN DEFAULT 0",
                "ALTER TABLE services ADD COLUMN sale_price REAL DEFAULT 0.0",
                "ALTER TABLE services ADD COLUMN sale_description TEXT",
                "ALTER TABLE services ADD COLUMN sale_status VARCHAR(20) DEFAULT 'unpublished'",
            ]

        for stmt in alter_statements:
            try:
                db.session.execute(text(stmt))
                field_name = stmt.split('ADD COLUMN ')[1].split(' ')[0]
                print(f"   - 添加字段 {field_name}")
            except Exception as e:
                if "Duplicate column name" in str(e) or "duplicate column name" in str(e).lower():
                    field_name = stmt.split('ADD COLUMN ')[1].split(' ')[0]
                    print(f"   - 字段 {field_name} 已存在，跳过")
                else:
                    print(f"   - 错误: {str(e)}")

        db.session.commit()

        # 2. 创建user_service_relations表
        print("2. 创建user_service_relations表...")

        if is_mysql:
            create_user_service_relations = """
                CREATE TABLE IF NOT EXISTS user_service_relations (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id VARCHAR(36) NOT NULL,
                    service_id VARCHAR(36) NOT NULL,
                    relation_type VARCHAR(20) NOT NULL,
                    purchase_time BIGINT,
                    purchase_price FLOAT,
                    create_time BIGINT NOT NULL,
                    INDEX idx_user_id (user_id),
                    INDEX idx_service_id (service_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        else:
            create_user_service_relations = """
                CREATE TABLE IF NOT EXISTS user_service_relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(36) NOT NULL,
                    service_id VARCHAR(36) NOT NULL,
                    relation_type VARCHAR(20) NOT NULL,
                    purchase_time BIGINT,
                    purchase_price REAL,
                    create_time BIGINT NOT NULL
                )
            """

        try:
            db.session.execute(text(create_user_service_relations))
            db.session.commit()
            print("   - 表 user_service_relations 创建成功")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("   - 表 user_service_relations 已存在，跳过")
            else:
                print(f"   - 错误: {str(e)}")

        # 3. 创建service_messages表
        print("3. 创建service_messages表...")

        if is_mysql:
            create_service_messages = """
                CREATE TABLE IF NOT EXISTS service_messages (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    service_id VARCHAR(36) NOT NULL,
                    sender_id VARCHAR(36) NOT NULL,
                    receiver_id VARCHAR(36) NOT NULL,
                    message_type VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT 0,
                    create_time BIGINT NOT NULL,
                    INDEX idx_service_id (service_id),
                    INDEX idx_receiver_id (receiver_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        else:
            create_service_messages = """
                CREATE TABLE IF NOT EXISTS service_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id VARCHAR(36) NOT NULL,
                    sender_id VARCHAR(36) NOT NULL,
                    receiver_id VARCHAR(36) NOT NULL,
                    message_type VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT 0,
                    create_time BIGINT NOT NULL
                )
            """

        try:
            db.session.execute(text(create_service_messages))
            db.session.commit()
            print("   - 表 service_messages 创建成功")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("   - 表 service_messages 已存在，跳过")
            else:
                print(f"   - 错误: {str(e)}")

        print("\n数据库迁移完成！")

if __name__ == "__main__":
    migrate()