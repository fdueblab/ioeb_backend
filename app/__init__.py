import logging
import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from config import config_by_name


def create_app(config_name):
    """
    创建Flask应用实例
    """
    app = Flask(__name__, static_folder="../static")
    app.config.from_object(config_by_name[config_name])

    # 设置日志级别
    app.logger.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 设置日志格式
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    console_handler.setFormatter(formatter)

    # 添加处理器到应用日志器
    app.logger.addHandler(console_handler)

    # 确保上传目录存在
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 注册CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # 注册蓝图
    from app.api import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    # 注册数据库
    from app.extensions import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    # 自动创建新表（如果不存在）
    with app.app_context():
        from app.models.service_message import ServiceMessage
        from app.models.user_service_relation import UserServiceRelation

        # 创建新表（如果不存在）
        db.create_all()

        # 自动为 services 表添加销售相关字段（如果不存在）
        from sqlalchemy import text, inspect
        inspector = inspect(db.engine)
        existing_columns = [c["name"] for c in inspector.get_columns("services")]
        sale_columns = {
            "is_for_sale": "BOOLEAN DEFAULT 0",
            "sale_price": "FLOAT DEFAULT 0.0",
            "sale_description": "TEXT",
            "sale_status": "VARCHAR(20) DEFAULT 'unpublished'",
        }
        for col_name, col_def in sale_columns.items():
            if col_name not in existing_columns:
                try:
                    db.session.execute(text(f"ALTER TABLE services ADD COLUMN {col_name} {col_def}"))
                    app.logger.info(f"已添加字段: services.{col_name}")
                except Exception as e:
                    app.logger.warning(f"添加字段 services.{col_name} 失败: {e}")
        db.session.commit()

    # 注册审计钩子：仅记录已认证 API 请求的元数据
    from app.services.audit_service import audit_service

    app.before_request(audit_service.attach_request_user)
    app.after_request(audit_service.log_request)

    # 初始化COS工具
    from app.utils.cos_utils import cos_utils

    cos_utils.init_app(app)

    # 初始化定时任务调度器
    from app.scheduler.tasks import init_scheduler

    init_scheduler(app)

    # 添加首页路由
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
