import json

from app.utils.mcp_artifact_utils import load_mcp_artifact_metadata


def test_missing_manifest_uses_legacy_sse_defaults(tmp_path):
    metadata = load_mcp_artifact_metadata(str(tmp_path))

    assert metadata["endpoint"] == "/sse"
    assert metadata["method"] == "sse"
    assert {tool["name"] for tool in metadata["tools"]} == {
        "healthCheck",
        "getServiceInfo",
    }


def test_v1_artifact_exposes_streamable_http_tool(tmp_path):
    manifest = {
        "artifactVersion": "ioeb.mcp-service-artifact/v1",
        "service": {
            "name": "repeat-text",
            "description": "Repeat text a requested number of times.",
        },
        "runtime": {
            "transport": "streamable-http",
            "endpoint": "/mcp",
        },
        "tool": {
            "name": "main_process",
            "description": "Repeat input text.",
        },
    }
    (tmp_path / "ioeb-service.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    metadata = load_mcp_artifact_metadata(str(tmp_path))

    assert metadata == {
        "endpoint": "/mcp",
        "method": "http",
        "description": "Repeat text a requested number of times.",
        "tools": [{
            "name": "main_process",
            "description": "Repeat input text.",
        }],
    }


def test_invalid_artifact_endpoint_cannot_escape_proxy_path(tmp_path):
    manifest = {
        "artifactVersion": "ioeb.mcp-service-artifact/v1",
        "runtime": {
            "transport": "streamable-http",
            "endpoint": "https://attacker.example/mcp",
        },
    }
    (tmp_path / "ioeb-service.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    metadata = load_mcp_artifact_metadata(str(tmp_path))

    assert metadata["endpoint"] == "/sse"
    assert metadata["method"] == "http"
