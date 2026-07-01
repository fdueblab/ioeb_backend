#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将数据库中待同步的意见反馈批量汇总到飞书多维表格。
供 GitHub Actions 定时任务或本地手动执行。
"""

import argparse
import datetime
import os
import sys

from sqlalchemy.exc import SQLAlchemyError

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.feedback import Feedback  # noqa: E402
from app.utils.flask_utils import get_flask_env  # noqa: E402
from scripts.feishu_client import FeishuClientError, feishu_client  # noqa: E402

BATCH_SIZE = 50
PENDING_STATUSES = ("pending", "failed")


def parse_args():
    parser = argparse.ArgumentParser(description="将待同步意见反馈批量写入飞书多维表格")
    parser.add_argument("--dry-run", action="store_true", help="仅统计待同步数量，不写入飞书")
    parser.add_argument("--limit", type=int, default=0, help="最多同步条数，0 表示不限制")
    return parser.parse_args()


def fetch_pending_feedbacks(limit=0):
    query = (
        Feedback.query.filter(Feedback.feishu_sync_status.in_(PENDING_STATUSES))
        .order_by(Feedback.created_at.asc())
    )
    if limit and limit > 0:
        query = query.limit(limit)
    return query.all()


def mark_synced(feedback, record_id):
    feedback.feishu_record_id = record_id
    feedback.feishu_sync_status = "synced"
    feedback.feishu_sync_error = None
    feedback.feishu_synced_at = int(datetime.datetime.now().timestamp() * 1000)


def mark_failed(feedback, error):
    feedback.feishu_sync_status = "failed"
    feedback.feishu_sync_error = str(error)[:1000]


def sync_batch(feedbacks):
    synced = 0
    failed = 0

    for index in range(0, len(feedbacks), BATCH_SIZE):
        batch = feedbacks[index : index + BATCH_SIZE]
        try:
            records = feishu_client.batch_create_records(batch)
            if len(records) != len(batch):
                raise FeishuClientError(
                    f"飞书返回记录数({len(records)})与请求数({len(batch)})不一致"
                )
            for feedback, record in zip(batch, records):
                mark_synced(feedback, record.get("record_id"))
            db.session.commit()
            synced += len(batch)
        except (FeishuClientError, SQLAlchemyError) as exc:
            db.session.rollback()
            for feedback in batch:
                mark_failed(feedback, exc)
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
            failed += len(batch)
            print(f"批次同步失败: {exc}")

    return synced, failed


def run_sync(dry_run=False, limit=0):
    if not dry_run and not feishu_client.is_configured():
        raise FeishuClientError("飞书同步配置不完整，请检查环境变量")

    pending_feedbacks = fetch_pending_feedbacks(limit=limit)
    total_pending = len(pending_feedbacks)
    print(f"待同步反馈数量: {total_pending}")

    if dry_run or total_pending == 0:
        return {"pending": total_pending, "synced": 0, "failed": 0}

    synced, failed = sync_batch(pending_feedbacks)
    print(f"同步完成: 成功 {synced} 条, 失败 {failed} 条")
    return {"pending": total_pending, "synced": synced, "failed": failed}


def main():
    args = parse_args()
    env = get_flask_env()
    app = create_app(env)

    with app.app_context():
        stats = run_sync(dry_run=args.dry_run, limit=args.limit)
        if args.dry_run:
            print("dry-run 模式，未写入飞书")
        print(stats)


if __name__ == "__main__":
    main()
