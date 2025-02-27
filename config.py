import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 算法代码配置
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制上传文件大小为16MB
    ALLOWED_EXTENSIONS = {'zip'}
    
    # 代码规范检查配置
    CODE_STANDARDS_CHECK = True  # 是否启用代码规范检查
    CODE_STANDARDS_STRICT = True  # 严格模式（True: 必须通过检查才处理，False: 仅警告）
    
    # 微服务生成服务配置
    REMOTE_SERVICE_URL = os.getenv('REMOTE_SERVICE_URL', 'http://localhost:8000/api/process')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    # 在生产环境中应该使用更安全的配置
    # 例如使用PostgreSQL或MySQL
    
    # 生产环境中更安全的算法代码上传设置
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 