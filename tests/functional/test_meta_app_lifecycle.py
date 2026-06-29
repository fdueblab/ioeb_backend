from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from app.extensions import db
from app.models import Service, ServiceApi
from app.services.meta_app_config import (
    ARTIFACT_SCHEMA,
    build_agent_only_artifact,
    default_runtime_spec,
    stable_hash,
)

# 跨端契约锚点：与 Micro-Agent tests/fixtures/golden_meta_app_artifact.json 同一份。
# 勿手改；常量与 MA tests/fixtures/golden.py 一致，漂移会让此处断言失败。
_GOLDEN_FIXTURE = Path(__file__).parent / "fixtures" / "golden_meta_app_artifact.json"
GOLDEN_ARTIFACT_ID = "app-37e3436d473b4479"
GOLDEN_ARTIFACT_HASH = "088f717621f73fbaf0d4a3accc661776633c8f5ef3042e2d48ec2e913607ad15"


def _artifact() -> dict:
    return json.loads(_GOLDEN_FIXTURE.read_text(encoding="utf-8"))


def _payload() -> dict:
    artifact = _artifact()
    return {
        "name": "Functional Meta App",
        "attribute": "intelligent",
        "type": "meta",
        "domain": "health",
        "industry": "",
        "scenario": "",
        "technology": "agent",
        "network": "ioeb_app-network",
        "port": "0.0.0.0:1021/TCP → 0.0.0.0:10021",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/aml/metaApp",
        "apiList": [{
            "name": "Functional Meta App",
            "url": "/api/agent/meta_app/run",
            "method": "sse",
            "parameterType": 1,
            "responseType": 1,
            "isFake": False,
            "services": [],
            "simulationBuildId": "build-functional",
            "metaAppArtifactId": artifact["artifactId"],
            "metaAppArtifactHash": stable_hash(artifact),
            "metaAppArtifact": artifact,
            "runMode": "agent",
            "runtimeSpec": default_runtime_spec(),
        }],
    }


def test_prepublish_persists_complete_runtime_contract(client, app):
    response = client.post("/api/services/prepublish", json=_payload())
    assert response.status_code == 201
    service = response.get_json()["service"]
    assert service["status"] == "pre_release_unrated"
    assert service["network"] == "ioeb_app-network"
    api = service["apiList"][0]
    assert api["simulationBuildId"] == "build-functional"
    assert api["metaAppArtifact"] == _artifact()
    assert api["metaAppArtifactId"] == GOLDEN_ARTIFACT_ID
    assert api["metaAppArtifactHash"] == GOLDEN_ARTIFACT_HASH
    assert api["runtimeSpec"]["docker"]["containerName"] == f"meta-app-{service['id']}"

    detail = client.get(f"/api/services/{service['id']}")
    assert detail.status_code == 200
    detail_api = detail.get_json()["service"]["apiList"][0]
    assert detail_api["metaAppArtifactId"] == GOLDEN_ARTIFACT_ID
    assert detail_api["metaAppArtifact"] == _artifact()


def test_missing_artifact_is_rejected(client, app):
    payload = _payload()
    payload["name"] = "Missing Artifact App"
    payload["apiList"][0].pop("metaAppArtifact")
    response = client.post("/api/services/prepublish", json=payload)
    assert response.status_code == 400
    assert "Artifact" in response.get_json()["message"]


def test_wrong_schema_is_rejected(client, app):
    payload = _payload()
    payload["name"] = "Wrong Schema App"
    payload["apiList"][0]["metaAppArtifact"]["schemaVersion"] = "legacy.v0"
    payload["apiList"][0]["metaAppArtifactHash"] = stable_hash(payload["apiList"][0]["metaAppArtifact"])
    response = client.post("/api/services/prepublish", json=payload)
    assert response.status_code == 400
    assert ARTIFACT_SCHEMA in response.get_json()["message"]


def _service_defaults(**overrides):
    base = {
        "attribute": "open_source",
        "domain": "health",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "18000/tcp",
        "volume": "",
        "status": "default",
        "number": 0,
        "deleted": 0,
        "create_time": 1,
        "creator_id": "",
    }
    base.update(overrides)
    return base


def test_migrate_meta_app_config_rebuilds_artifact(app):
    dep_id = f"dep-{uuid.uuid4().hex[:8]}"
    meta_id = f"meta-{uuid.uuid4().hex[:8]}"
    stale = {"schemaVersion": "legacy.v0", "artifactId": "stale", "runtime": {"serviceBindings": []}}

    with app.app_context():
        db.session.add(Service(id=dep_id, name="Dep MCP", type="atomic_mcp", **_service_defaults()))
        db.session.add(ServiceApi(
            id=str(uuid.uuid4()),
            service_id=dep_id,
            name="Dep MCP",
            url="https://fdueblab.cn/mcp-proxy/18000/sse",
            method="sse",
            des="dep",
            parameter_type=0,
            response_type=0,
            is_fake=False,
        ))
        db.session.add(Service(id=meta_id, name="Legacy Meta", type="meta", **_service_defaults()))
        db.session.add(ServiceApi(
            id=str(uuid.uuid4()),
            service_id=meta_id,
            name="Legacy Meta",
            url="/api/agent/meta_app/run",
            method="sse",
            des="meta",
            parameter_type=1,
            response_type=1,
            is_fake=False,
            services=dep_id,
            meta_app_artifact=stale,
            meta_app_artifact_id="stale",
            meta_app_artifact_hash="deadbeef",
            simulation_build_id="old-build",
        ))
        db.session.commit()

        from app.services.meta_app_config import migrate_meta_app_services

        migrate_meta_app_services()

        meta = db.session.get(Service, meta_id)
        api = meta.apis[0]
        expected = build_agent_only_artifact(meta, api, [db.session.get(Service, dep_id)])
        assert api.meta_app_artifact["schemaVersion"] == ARTIFACT_SCHEMA
        assert api.meta_app_artifact != stale
        assert api.meta_app_artifact_id == expected["artifactId"]
        assert api.meta_app_artifact_hash == stable_hash(expected)
        assert api.simulation_build_id == f"migration-{meta_id}"
        assert meta.status == "pre_release_unrated"


def test_invalid_artifact_does_not_create_service(client, app):
    payload = _payload()
    payload["name"] = "Invalid Meta App"
    payload["apiList"][0]["metaAppArtifactHash"] = "invalid"
    with app.app_context():
        before = Service.query.filter_by(name="Invalid Meta App").count()
    response = client.post("/api/services/prepublish", json=payload)
    assert response.status_code == 400
    with app.app_context():
        assert Service.query.filter_by(name="Invalid Meta App").count() == before


def test_meta_app_deploy_reaches_pending_status(client, app):
    response = client.post("/api/services/prepublish", json=_payload())
    service_id = response.get_json()["service"]["id"]
    app.config["META_APP_DEPLOY_DELAY_SECONDS"] = 0.01

    deployed = client.get(f"/api/services/{service_id}/deploy")
    assert deployed.status_code == 200
    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Service, service_id).status == "deploying"

    time.sleep(0.05)
    with app.app_context():
        db.session.expire_all()
        assert db.session.get(Service, service_id).status == "pre_release_pending"
