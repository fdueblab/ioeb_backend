from flask import Flask, send_from_directory
from flask_cors import CORS
from config import config_by_name
import os

def create_app(config_name):
    """
    创建Flask应用实例
    """
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_by_name[config_name])
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 注册CORS
    CORS(app)
    
    # 注册蓝图
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 注册数据库
    from app.extensions import db
    db.init_app(app)
    
    # 添加首页路由
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    return app 