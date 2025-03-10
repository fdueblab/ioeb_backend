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
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
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
    from app.extensions import db

    db.init_app(app)

    # 添加首页路由
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
