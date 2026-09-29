"""众智工场复用后端时的草稿和消息权限回归测试。"""

import datetime
import io
import zipfile

import pytest
from werkzeug.datastructures import FileStorage

from app import create_app
from app.extensions import db
from app.models import Role, User, UserToken


@pytest.fixture
def marketplace_client():
    app = create_app("testing")
    now = int(datetime.datetime.now().timestamp() * 1000)
    with app.test_client() as client, app.app_context():
        db.session.add(Role(id="user", name="用户", describe="普通用户", status=1, deleted=0, create_time=now))
        db.session.add(Role(id="admin", name="管理员", describe="管理员", status=1, deleted=0, create_time=now))
        for user_id in ("supplier", "buyer", "outsider", "admin"):
            db.session.add(User(
                id=user_id, username=user_id, name=user_id, password="x",
                role_id="admin" if user_id == "admin" else "user",
                status=1, deleted=0, create_time=now,
            ))
            db.session.add(UserToken(
                user_id=user_id, token=f"{user_id}-token", expires_at=now + 86400000,
            ))
        db.session.commit()
        yield client
        db.session.remove()
        db.drop_all()


def auth(user_id):
    return {"Access-Token": f"{user_id}-token"}


def test_mcp_packaging_job_owner_and_confirmed_tools(marketplace_client, monkeypatch, tmp_path):
    """Uploaded source and tool choices belong to the signed-in supplier."""
    monkeypatch.setenv("MCP_PACKAGING_BASE_PATH", str(tmp_path))
    client = marketplace_client
    assert client.post("/api/mcp-packaging/jobs", json={}).status_code == 401

    created = client.post("/api/mcp-packaging/jobs", headers=auth("supplier"), json={})
    assert created.status_code == 201, created.get_json()
    job = created.get_json()["job"]
    job_id = job["id"]
    assert client.get(f"/api/mcp-packaging/jobs/{job_id}", headers=auth("buyer")).status_code == 404
    assert client.put(f"/api/mcp-packaging/jobs/{job_id}/source", headers=auth("buyer"),
                      data={"file": (io.BytesIO(b"def stolen(): pass"), "bad.py")},
                      content_type="multipart/form-data").status_code == 404

    uploaded = client.put(f"/api/mcp-packaging/jobs/{job_id}/source", headers=auth("supplier"),
                          data={"file": (io.BytesIO(b"def score(value):\n    return value\n"), "model.py")},
                          content_type="multipart/form-data")
    assert uploaded.status_code == 200, uploaded.get_json()
    job = uploaded.get_json()["job"]
    assert [candidate["entrypoint"] for candidate in job["candidates"]] == ["source.py:score"]
    assert client.post(f"/api/mcp-packaging/jobs/{job_id}/package", headers=auth("supplier")).status_code == 400

    invalid = client.patch(f"/api/mcp-packaging/jobs/{job_id}", headers=auth("supplier"), json={
        "revision": job["revision"], "spec": {"service_name": "评分", "scenario": "分析输入",
                                       "tools": [{"entrypoint": "source.py:nonexistent", "name": "invented",
                                                  "input_schema": {"type": "object"}}]},
    })
    assert invalid.status_code == 400
    saved = client.patch(f"/api/mcp-packaging/jobs/{job_id}", headers=auth("supplier"), json={
        "revision": job["revision"], "spec": {"service_name": "评分", "scenario": "分析输入",
                                       "tools": [{"entrypoint": "source.py:score", "name": "score",
                                                  "input_schema": {"type": "object", "properties": {"value": {"type": "string"}}}}]},
    })
    assert saved.status_code == 200, saved.get_json()
    assert saved.get_json()["job"]["revision"] == job["revision"] + 1
    assert client.patch(f"/api/mcp-packaging/jobs/{job_id}", headers=auth("supplier"),
                        json={"revision": job["revision"], "spec": {}}).status_code == 409


def test_generated_mcp_package_rejects_dangerous_compose():
    from app.api.namespaces.mcp_packaging_ns import _validate_package

    def archive(compose):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zipped:
            zipped.writestr("output/server.py", "")
            zipped.writestr("output/Dockerfile", "FROM python:3.10-slim")
            zipped.writestr("output/docker-compose.yml", compose)
        return buffer.getvalue()

    _validate_package(archive("services:\n  mcp:\n    build: .\n    ports: ['8000:8000']\n"))
    with pytest.raises(ValueError, match="不允许"):
        _validate_package(archive("services:\n  mcp:\n    build: .\n    privileged: true\n    ports: ['8000:8000']\n"))
    with pytest.raises(ValueError, match="不允许"):
        _validate_package(archive("services:\n  mcp:\n    build: .\n    volumes: ['/var/run/docker.sock:/var/run/docker.sock']\n    ports: ['8000:8000']\n"))


def test_mcp_package_download_and_deploy_are_owner_scoped_and_idempotent(marketplace_client, monkeypatch, tmp_path):
    """The downloadable artifact is private and duplicate deploy clicks reuse one service."""
    import app.api.namespaces.mcp_packaging_ns as mcp_ns

    monkeypatch.setenv("MCP_PACKAGING_BASE_PATH", str(tmp_path))
    client = marketplace_client
    created = client.post("/api/mcp-packaging/jobs", headers=auth("supplier"), json={}).get_json()["job"]
    job_id = created["id"]
    uploaded = client.put(f"/api/mcp-packaging/jobs/{job_id}/source", headers=auth("supplier"),
                          data={"file": (io.BytesIO(b"def score(value):\n    return value\n"), "model.py")},
                          content_type="multipart/form-data").get_json()["job"]
    spec = {"service_name": "评分工具", "scenario": "给输入评分", "tools": [
        {"entrypoint": "source.py:score", "name": "score",
         "input_schema": {"type": "object", "properties": {"value": {"type": "string"}}, "required": ["value"]}}]}
    assert client.patch(f"/api/mcp-packaging/jobs/{job_id}", headers=auth("supplier"),
                        json={"revision": uploaded["revision"], "spec": spec}).status_code == 200

    package = io.BytesIO()
    with zipfile.ZipFile(package, "w") as zipped:
        zipped.writestr("output/server.py", "print('server')")
        zipped.writestr("output/Dockerfile", "FROM python:3.10-slim")
        zipped.writestr("output/docker-compose.yml", "services:\n  mcp:\n    build: .\n    ports: ['8000:8000']\n")

    def fake_package(_path, _spec, progress):
        progress("task-1", "已接收")
        return package.getvalue()

    class ImmediateThread:
        def __init__(self, target, args, daemon):
            self.target, self.args = target, args

        def start(self):
            self.target(*self.args)

    monkeypatch.setattr(mcp_ns, "_agent_package", fake_package)
    monkeypatch.setattr(mcp_ns.threading, "Thread", ImmediateThread)
    generated = client.post(f"/api/mcp-packaging/jobs/{job_id}/package", headers=auth("supplier"))
    assert generated.status_code == 202, generated.get_json()
    assert client.get(f"/api/mcp-packaging/jobs/{job_id}/artifact", headers=auth("buyer")).status_code == 404
    artifact = client.get(f"/api/mcp-packaging/jobs/{job_id}/artifact", headers=auth("supplier"))
    assert artifact.status_code == 200
    assert zipfile.is_zipfile(io.BytesIO(artifact.data))

    calls = []

    def fake_deploy(file, data):
        calls.append((file.filename, data["creator_id"]))
        return {"id": "only-one-service"}

    monkeypatch.setattr(mcp_ns.service_service, "upload_and_deploy_service", fake_deploy)
    first = client.post(f"/api/mcp-packaging/jobs/{job_id}/deploy", headers=auth("supplier"))
    second = client.post(f"/api/mcp-packaging/jobs/{job_id}/deploy", headers=auth("supplier"))
    assert first.status_code == 202, first.get_json()
    assert second.get_json()["serviceId"] == "only-one-service"
    assert calls == [("mcp-service-package.zip", "supplier")]


def test_mcp_source_algorithm_uses_owner_only(marketplace_client):
    client = marketplace_client
    algorithm_id = create_algorithm(client, "draft")
    uploaded = client.post("/api/services/scenario-generated/upload", headers=auth("supplier"),
                           data={"file": (io.BytesIO(b"def score(value):\n    return value\n"), "algorithm.py"),
                                 "name": "已有算法", "domain": "aml", "draft_id": algorithm_id},
                           content_type="multipart/form-data")
    assert uploaded.status_code == 201, uploaded.get_json()
    assert client.post("/api/mcp-packaging/jobs", headers=auth("buyer"),
                       json={"sourceServiceId": algorithm_id}).status_code == 403
    created = client.post("/api/mcp-packaging/jobs", headers=auth("supplier"),
                          json={"sourceServiceId": algorithm_id})
    assert created.status_code == 201, created.get_json()
    assert created.get_json()["job"]["sourceServiceId"] == algorithm_id
    assert created.get_json()["job"]["candidates"][0]["name"] == "score"


def create_algorithm(client, status):
    response = client.post("/api/services", headers=auth("supplier"), json={
        "name": "测试算法", "attribute": "custom", "type": "generated_algorithm",
        "domain": "aml", "industry": "", "scenario": "", "technology": "AI",
        "network": "n/a", "port": "n/a", "volume": "n/a", "status": status,
        "source": {"companyIntroduce": "ZZF_DRAFT_V1:{}", "msIntroduce": "测试描述"},
    })
    assert response.status_code == 201, response.get_json()
    return response.get_json()["service"]["id"]


def test_draft_is_private_and_can_be_completed(marketplace_client, monkeypatch):
    client = marketplace_client
    draft_id = create_algorithm(client, "draft")

    assert client.get(f"/api/services/{draft_id}").status_code == 404
    assert client.get(f"/api/services/{draft_id}", headers=auth("buyer")).status_code == 404
    assert client.get(f"/api/services/{draft_id}", headers=auth("supplier")).status_code == 200
    assert client.post(f"/api/services/{draft_id}", headers=auth("buyer"), json={"name": "劫持"}).status_code == 403
    assert client.post(f"/api/services/{draft_id}", headers=auth("supplier"), json={"status": "released"}).status_code == 400

    for headers, count in (({}, 0), (auth("buyer"), 0), (auth("supplier"), 1)):
        response = client.get("/api/services/filter?type=generated_algorithm&page=1&pageSize=10", headers=headers)
        assert response.status_code == 200
        assert response.get_json()["total"] == count

    batch = client.post("/api/services/batch", json={"ids": [draft_id]})
    assert batch.status_code == 200
    assert batch.get_json()["services"] == []

    with monkeypatch.context() as patch:
        def fail_save(_file, _destination):
            raise OSError("模拟磁盘写入失败")

        patch.setattr(FileStorage, "save", fail_save)
        failed = client.post(
            "/api/services/scenario-generated/upload", headers=auth("supplier"),
            data={
                "file": (io.BytesIO(b"def run(x):\n    return x\n"), "algorithm.py"),
                "name": "被中断的商品", "domain": "aml", "draft_id": draft_id,
            },
            content_type="multipart/form-data",
        )
    assert failed.status_code == 400
    restored = client.get(f"/api/services/{draft_id}", headers=auth("supplier")).get_json()["service"]
    assert restored["status"] == "draft"
    assert restored["name"] == "测试算法"
    assert restored["source"]["companyIntroduce"] == "ZZF_DRAFT_V1:{}"

    uploaded = client.post(
        "/api/services/scenario-generated/upload", headers=auth("supplier"),
        data={
            "file": (io.BytesIO(b"def run(x):\n    return x\n"), "algorithm.py"),
            "name": "测试算法", "domain": "aml", "draft_id": draft_id,
        },
        content_type="multipart/form-data",
    )
    assert uploaded.status_code == 201, uploaded.get_json()
    assert uploaded.get_json()["service"]["id"] == draft_id
    assert client.get(f"/api/services/{draft_id}/scenario-generated-code", headers=auth("buyer")).status_code == 403
    assert client.get(f"/api/services/{draft_id}/scenario-generated-code", headers=auth("supplier")).status_code == 200


def test_messages_are_limited_to_participants(marketplace_client):
    client = marketplace_client
    service_id = create_algorithm(client, "not_deployed")
    assert client.post(f"/api/services/{service_id}", headers=auth("admin"), json={"name": "管理员维护的算法"}).status_code == 200
    sent = client.post("/api/messages/contact-purchase", headers=auth("buyer"), json={
        "serviceId": service_id, "content": "请问支持 CSV 吗？",
    })
    assert sent.status_code == 201, sent.get_json()
    message_id = sent.get_json()["data"]["id"]

    assert len(client.get("/api/messages/user", headers=auth("buyer")).get_json()["messages"]) == 1
    assert len(client.get("/api/messages/user", headers=auth("supplier")).get_json()["messages"]) == 1
    assert client.get("/api/messages/user", headers=auth("outsider")).get_json()["messages"] == []
    assert client.get(f"/api/messages/service/{service_id}", headers=auth("outsider")).get_json()["messages"] == []
    assert client.post(f"/api/messages/{message_id}/reply", headers=auth("outsider"), json={"content": "冒充回复"}).status_code == 403

    replied = client.post(f"/api/messages/{message_id}/reply", headers=auth("supplier"), json={"content": "支持"})
    assert replied.status_code == 201, replied.get_json()
    assert len(client.get("/api/messages/user", headers=auth("buyer")).get_json()["messages"]) == 2
