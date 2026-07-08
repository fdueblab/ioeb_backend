#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""元应用配置独立表迁移（幂等，可对任意目标库重复执行）。

将元应用运行契约/展示层字段从 service_apis 迁至独立表 meta_app_configs：

  1) 建出 meta_app_configs（存在则跳过）；
  2) 退役旧形态下的历史元应用记录（严格限定 type='meta'，连同从属记录物理删除，
     日后经“仿真构建 → 预发布”重新生成）；
  3) 删除 service_apis 上已废弃的元应用列（逐列“存在才删”，幂等）。

用法（加载目标环境变量后）：
  python scripts/migrate_meta_app_config_table.py

应在维护窗口内使用新代码执行，并在新业务进程启动前完成。
"""

import os
import sys

from sqlalchemy import inspect, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models import (
    MetaAppConfig,
    Service,
    ServiceApi,
    ServiceApiParameter,
    ServiceApiTool,
    ServiceNorm,
    ServiceSource,
)
from app.utils.flask_utils import get_flask_env


_OBSOLETE_META_COLUMNS = [
    "subtitle",
    "services",
    "input_name",
    "output_name",
    "output_visualization",
    "submit_button_text",
    "simulation_build_id",
    "meta_app_artifact_id",
    "meta_app_artifact_hash",
    "meta_app_artifact",
    "run_mode",
    "runtime_spec",
]


def ensure_table():
    MetaAppConfig.__table__.create(db.engine, checkfirst=True)
    print("[1/3] meta_app_configs 已就绪")


def retire_legacy_meta_services():
    meta_ids = [
        row[0] for row in db.session.query(Service.id).filter(Service.type == "meta").all()
    ]
    if not meta_ids:
        print("[2/3] 无历史元应用记录，跳过退役")
        return

    for service_id in meta_ids:
        api_ids = [
            row[0]
            for row in db.session.query(ServiceApi.id)
            .filter(ServiceApi.service_id == service_id)
            .all()
        ]
        if api_ids:
            ServiceApiParameter.query.filter(
                ServiceApiParameter.api_id.in_(api_ids)
            ).delete(synchronize_session=False)
            ServiceApiTool.query.filter(
                ServiceApiTool.api_id.in_(api_ids)
            ).delete(synchronize_session=False)
        ServiceApi.query.filter_by(service_id=service_id).delete(synchronize_session=False)
        ServiceNorm.query.filter_by(service_id=service_id).delete(synchronize_session=False)
        ServiceSource.query.filter_by(service_id=service_id).delete(synchronize_session=False)
        MetaAppConfig.query.filter_by(service_id=service_id).delete(synchronize_session=False)

    Service.query.filter(Service.id.in_(meta_ids)).delete(synchronize_session=False)
    db.session.commit()
    print(f"[2/3] 已退役 {len(meta_ids)} 个历史元应用（含从属记录）")


def drop_obsolete_columns():
    existing = {column["name"] for column in inspect(db.engine).get_columns("service_apis")}
    to_drop = [name for name in _OBSOLETE_META_COLUMNS if name in existing]
    if not to_drop:
        print("[3/3] service_apis 无废弃元应用列，跳过")
        return

    with db.engine.begin() as connection:
        for name in to_drop:
            connection.execute(text(f"ALTER TABLE service_apis DROP COLUMN {name}"))
    print(f"[3/3] 已从 service_apis 删除废弃列：{', '.join(to_drop)}")


def main():
    app = create_app(get_flask_env())
    with app.app_context():
        print(f"目标库: {db.engine.url}")
        ensure_table()
        retire_legacy_meta_services()
        drop_obsolete_columns()
        print("迁移完成")


if __name__ == "__main__":
    main()
