"""Read runtime metadata from deterministic MCP service artifacts."""

import json
import re
from pathlib import Path
from typing import Dict


ARTIFACT_VERSION = "ioeb.mcp-service-artifact/v1"
DEFAULT_METADATA = {
    "endpoint": "/sse",
    "method": "sse",
    "description": "",
    "tools": [
        {
            "name": "healthCheck",
            "description": "判断微服务状态是否正常可用",
        },
        {
            "name": "getServiceInfo",
            "description": "获取服务信息和能力描述",
        },
    ],
}
_SAFE_ENDPOINT = re.compile(r"^/[A-Za-z0-9._~/-]*$")
_HTTP_TRANSPORTS = {"http", "streamable-http", "streamable_http"}


def _safe_endpoint(value: object) -> str:
    if not isinstance(value, str) or not _SAFE_ENDPOINT.fullmatch(value):
        return DEFAULT_METADATA["endpoint"]
    if "//" in value or ".." in value.split("/"):
        return DEFAULT_METADATA["endpoint"]
    return value


def load_mcp_artifact_metadata(project_root: str) -> Dict:
    """Return deploy metadata, retaining legacy SSE defaults when no v1 artifact exists."""
    metadata = {
        **DEFAULT_METADATA,
        "tools": [dict(tool) for tool in DEFAULT_METADATA["tools"]],
    }
    manifest_path = Path(project_root) / "ioeb-service.json"
    if not manifest_path.is_file():
        return metadata

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return metadata
    if not isinstance(manifest, dict) or manifest.get("artifactVersion") != ARTIFACT_VERSION:
        return metadata

    runtime = manifest.get("runtime")
    runtime = runtime if isinstance(runtime, dict) else {}
    transport = str(runtime.get("transport", "sse")).strip().lower()
    endpoint = _safe_endpoint(runtime.get("endpoint"))
    method = "http" if transport in _HTTP_TRANSPORTS else "sse"

    service = manifest.get("service")
    service = service if isinstance(service, dict) else {}
    description = service.get("description")
    description = description.strip() if isinstance(description, str) else ""

    tool = manifest.get("tool")
    tools = []
    if isinstance(tool, dict):
        name = tool.get("name")
        tool_description = tool.get("description")
        if isinstance(name, str) and name.strip():
            tools.append({
                "name": name.strip(),
                "description": (
                    tool_description.strip()
                    if isinstance(tool_description, str)
                    else ""
                ),
            })

    metadata.update({
        "endpoint": endpoint,
        "method": method,
        "description": description,
    })
    if tools:
        metadata["tools"] = tools
    return metadata
