import json

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    """创建测试客户端"""
    app = create_app("testing")

    # 创建测试数据库上下文
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert "message" in data


def test_get_users_empty(client):
    """测试获取用户列表（空列表）"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["users"] == []


def test_create_and_get_user(client):
    """测试创建和获取用户"""
    # 创建测试用户
    user_data = {"username": "测试用户", "email": "test@example.com"}

    # 创建用户
    response = client.post(
        "/api/users", data=json.dumps(user_data), content_type="application/json"
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["message"] == "用户创建成功"
    assert data["user"]["username"] == user_data["username"]
    assert data["user"]["email"] == user_data["email"]

    # 获取用户列表
    response = client.get("/api/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["users"]) == 1
    assert data["users"][0]["username"] == user_data["username"]
