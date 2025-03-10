import os
from datetime import timedelta


class Config:
    """基础配置"""

    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    # JWT配置
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 算法代码配置
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制上传文件大小为16MB
    ALLOWED_EXTENSIONS = {"zip"}

    # 代码规范检查配置
    CODE_STANDARDS_CHECK = True  # 是否启用代码规范检查
    CODE_STANDARDS_STRICT = True  # 严格模式（True: 必须通过检查才处理，False: 仅警告）

    # 微服务生成服务配置
    REMOTE_SERVICE_URL = os.getenv("REMOTE_SERVICE_URL", "http://localhost:8000/api/process")


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True

    username = os.getenv("DB_USERNAME", "default_username")
    password = os.getenv("DB_PASSWORD", "default_password")
    host = os.getenv("DB_HOST", "sh-cynosdbmysql-grp-gfzuhdpw.sql.tencentcdb.com")
    port = os.getenv("DB_PORT", "22254")
    database = os.getenv("DB_NAME", "ioeb-dev")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"


class TestingConfig(Config):
    """测试环境配置"""

    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """生产环境配置"""

    DEBUG = False

    username = os.getenv("DB_USERNAME", "default_username")
    password = os.getenv("DB_PASSWORD", "default_password")
    host = os.getenv("DB_HOST", "sh-cynosdbmysql-grp-gfzuhdpw.sql.tencentcdb.com")
    port = os.getenv("DB_PORT", "22254")
    database = os.getenv("DB_NAME", "ioeb-prod")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

    # 生产环境中更安全的算法代码上传设置
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
