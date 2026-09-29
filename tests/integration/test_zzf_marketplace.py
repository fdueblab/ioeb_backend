"""众智工场复用后端时的草稿和消息权限回归测试。"""

import datetime
import io

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
