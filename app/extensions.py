from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 初始化SQLAlchemy
db = SQLAlchemy()

# 初始化迁移工具
migrate = Migrate()
