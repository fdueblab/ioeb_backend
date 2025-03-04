import os

from app import create_app
from app.extensions import db, migrate

# 获取环境配置
env = os.getenv("FLASK_ENV", "default")
app = create_app(env)

# 添加数据库迁移支持
migrate.init_app(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
