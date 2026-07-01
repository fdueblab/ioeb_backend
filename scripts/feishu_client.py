"""
飞书开放平台客户端（脚本专用）
用于定时任务将意见反馈批量同步到飞书多维表格。
"""

import datetime
import os
import time
from typing import Dict, List, Optional

import requests


class FeishuClientError(Exception):
    """飞书客户端异常"""


class FeishuClient:
    """飞书多维表格 API 客户端"""

    FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

    def __init__(self):
        self._tenant_access_token: Optional[str] = None
        self._token_expire_at = 0

    def is_configured(self) -> bool:
        required_keys = (
            "FEISHU_APP_ID",
            "FEISHU_APP_SECRET",
            "FEISHU_BITABLE_APP_TOKEN",
            "FEISHU_BITABLE_TABLE_ID",
        )
        return all(os.getenv(key) for key in required_keys)

    def get_tenant_access_token(self) -> str:
        now = int(time.time())
        if self._tenant_access_token and now < self._token_expire_at:
            return self._tenant_access_token

        app_id = os.getenv("FEISHU_APP_ID")
        app_secret = os.getenv("FEISHU_APP_SECRET")
        response = requests.post(
            f"{self.FEISHU_API_BASE}/auth/v3/tenant_access_token/internal",
            json={"app_id": app_id, "app_secret": app_secret},
            timeout=15,
        )
        result = self._parse_response(response, "获取飞书 tenant_access_token 失败")
        token = result.get("tenant_access_token")
        if not token:
            raise FeishuClientError("飞书 token 响应缺少 tenant_access_token")

        expire = int(result.get("expire", 7200))
        self._tenant_access_token = token
        self._token_expire_at = now + max(expire - 300, 60)
        return token

    def build_feedback_fields(self, feedback) -> Dict:
        return {
            "反馈ID": feedback.id,
            "提交用户": feedback.username or "匿名用户",
            "反馈内容": feedback.content,
            "提交时间": self._format_timestamp(feedback.created_at),
            "处理状态": "待处理",
        }

    def batch_create_records(self, feedbacks: List) -> List[Dict]:
        if not feedbacks:
            return []

        if not self.is_configured():
            raise FeishuClientError("飞书同步配置不完整")

        token = self.get_tenant_access_token()
        app_token = os.getenv("FEISHU_BITABLE_APP_TOKEN")
        table_id = os.getenv("FEISHU_BITABLE_TABLE_ID")
        url = (
            f"{self.FEISHU_API_BASE}/bitable/v1/apps/{app_token}"
            f"/tables/{table_id}/records/batch_create"
        )
        records = [{"fields": self.build_feedback_fields(item)} for item in feedbacks]
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={"records": records},
            timeout=30,
        )
        result = self._parse_response(response, "飞书多维表格批量新增反馈记录失败")
        return (result.get("data") or {}).get("records") or []

    def _format_timestamp(self, timestamp_ms: Optional[int]) -> str:
        if not timestamp_ms:
            return ""
        dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def _parse_response(self, response, error_prefix: str) -> Dict:
        try:
            result = response.json()
        except ValueError as exc:
            raise FeishuClientError(f"{error_prefix}: 响应不是有效 JSON") from exc

        if response.status_code >= 400 or result.get("code") not in (0, None):
            message = result.get("msg") or result.get("message") or response.text
            raise FeishuClientError(f"{error_prefix}: {message}")
        return result


feishu_client = FeishuClient()
