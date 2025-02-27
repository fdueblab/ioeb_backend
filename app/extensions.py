from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化SQLAlchemy
db = SQLAlchemy()

# 初始化迁移工具
migrate = Migrate() 