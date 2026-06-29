"""本地联调 backend：SQLite 文件库 + manage.py 全量 mock，不连 dev MySQL。

  cd ioeb_backend
  set -a && source .env_dev && set +a
  .venv/bin/python wsgi_verify.py

等价于 db.sh 的 create_db + seed_db，并追加 service_catalog.json 医疗 MCP（**mcp-proxy 远程 URL**）。

登录：admin / 123456

prepublish 后查库：
  sqlite3 local_verify.db "SELECT simulation_build_id, meta_app_artifact_id, meta_app_artifact_hash, run_mode FROM service_apis ORDER BY rowid DESC LIMIT 1;"
"""

import os

import app.models  # noqa: F401 — 注册 ORM
from app import create_app
from app.extensions import db, migrate
from app.models import Service
from config import TestingConfig, config_by_name
from mocks.seed import seed_all_mock_data, seed_mcp_catalog

_DB_PATH = os.path.join(os.path.dirname(__file__), "local_verify.db")


class LocalVerifyConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{_DB_PATH}"


config_by_name["local_verify"] = LocalVerifyConfig

app = create_app("local_verify")
migrate.init_app(app, db)


def _ensure_schema_and_seed():
    db.create_all()
    if Service.query.count() == 0:
        db.drop_all()
        db.create_all()
        seed_all_mock_data()
    seed_mcp_catalog()


with app.app_context():
    _ensure_schema_and_seed()

if __name__ == "__main__":
    print(f"local DB: {_DB_PATH}")
    app.run(host="0.0.0.0", port=5000, use_reloader=False, debug=False)
