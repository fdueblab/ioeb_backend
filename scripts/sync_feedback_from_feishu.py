#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从飞书多维表格拉取意见反馈的处理状态与处理总结，回写到数据库。
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


def parse_args():
    parser = argparse.ArgumentParser(description="从飞书多维表格拉取反馈处理结果")
    parser.add_argument("--dry-run", action="store_true", help="仅统计可拉取数量，不写库")
    parser.add_argument("--limit", type=int, default=0, help="最多处理条数，0 表示不限制")
    return parser.parse_args()


def fetch_synced_feedbacks(limit=0):
    query = (
        Feedback.query.filter(
            Feedback.feishu_sync_status == "synced",
            Feedback.feishu_record_id.isnot(None),
        )
        .order_by(Feedback.created_at.asc())
    )
    if limit and limit > 0:
        query = query.limit(limit)
    return query.all()


def apply_parsed_fields(feedback, parsed, dry_run=False) -> bool:
    changed = False
    feishu_status = parsed.get("feishu_status") or ""
    response_summary = parsed.get("response_summary") or ""
    db_status = parsed.get("db_status")

    if feishu_status and feedback.feishu_status != feishu_status:
        changed = True
        if not dry_run:
            feedback.feishu_status = feishu_status

    if db_status and feedback.status != db_status:
        changed = True
        if not dry_run:
            feedback.status = db_status

    if response_summary and feedback.response_summary != response_summary:
        changed = True
        if not dry_run:
            feedback.response_summary = response_summary
            if not feedback.responded_at:
                feedback.responded_at = int(datetime.datetime.now().timestamp() * 1000)

    return changed


def run_pull(dry_run=False, limit=0):
    if not dry_run and not feishu_client.is_configured():
        raise FeishuClientError("飞书同步配置不完整，请检查环境变量")

    feedbacks = fetch_synced_feedbacks(limit=limit)
    total = len(feedbacks)
    print(f"可拉取反馈数量: {total}")

    if total == 0:
        return {"total": 0, "updated": 0, "unchanged": 0, "failed": 0}

    updated = 0
    unchanged = 0
    failed = 0

    for index in range(0, total, BATCH_SIZE):
        batch = feedbacks[index : index + BATCH_SIZE]
        record_ids = [item.feishu_record_id for item in batch if item.feishu_record_id]
        if not record_ids:
            continue

        try:
            if dry_run:
                print(f"dry-run: 将拉取 {len(record_ids)} 条飞书记录")
                updated += len(record_ids)
                continue

            records = feishu_client.batch_get_records(record_ids)
            record_map = {item.get("record_id"): item for item in records}

            for feedback in batch:
                record = record_map.get(feedback.feishu_record_id)
                if not record:
                    failed += 1
                    continue
                parsed = feishu_client.parse_feedback_record_fields(record)
                if apply_parsed_fields(feedback, parsed):
                    updated += 1
                else:
                    unchanged += 1

            db.session.commit()
        except (FeishuClientError, SQLAlchemyError) as exc:
            db.session.rollback()
            failed += len(batch)
            print(f"批次拉取失败: {exc}")

    print(f"拉取完成: 更新 {updated} 条, 无变化 {unchanged} 条, 失败 {failed} 条")
    return {
        "total": total,
        "updated": updated,
        "unchanged": unchanged,
        "failed": failed,
    }


def main():
    args = parse_args()
    env = get_flask_env()
    app = create_app(env)

    with app.app_context():
        stats = run_pull(dry_run=args.dry_run, limit=args.limit)
        if args.dry_run:
            print("dry-run 模式，未写入数据库")
        print(stats)


if __name__ == "__main__":
    main()
