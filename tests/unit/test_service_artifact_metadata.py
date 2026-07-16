import json

from app.services.service_service import ServiceService


def test_load_mcp_artifact_metadata_reads_agent_plan(tmp_path):
    (tmp_path / "ioeb-service.json").write_text(
        json.dumps({"endpoint": "/custom-sse"}),
        encoding="utf-8"
    )
    (tmp_path / "packaging_plan.json").write_text(
        json.dumps({
            "schemaVersion": "ioeb.agentic-mcp-plan/v1",
            "services": [
                {
                    "tools": [
                        {"name": "predict_risk", "description": "预测风险"},
                        {"name": "explain_risk", "description": "解释风险"}
                    ]
                },
                {
                    "tools": [
                        {"name": "predict_risk", "description": "重复项"},
                        {"name": "batch_score", "description": "批量评分"}
                    ]
                }
            ]
        }),
        encoding="utf-8"
    )

    metadata = ServiceService._load_mcp_artifact_metadata(str(tmp_path))

    assert metadata["endpoint"] == "/custom-sse"
    assert [tool["name"] for tool in metadata["tools"]] == [
        "predict_risk",
        "explain_risk",
        "batch_score"
    ]


def test_load_mcp_artifact_metadata_has_safe_fallbacks(tmp_path):
    (tmp_path / "ioeb-service.json").write_text(
        json.dumps({"endpoint": "/../internal?token=secret"}),
        encoding="utf-8"
    )
    (tmp_path / "packaging_plan.json").write_text("not-json", encoding="utf-8")

    metadata = ServiceService._load_mcp_artifact_metadata(str(tmp_path))

    assert metadata == {"endpoint": "/sse", "tools": []}
