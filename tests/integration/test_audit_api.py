import datetime
import json

import pytest

from app import create_app
from app.extensions import db
from app.models import Role, RolePermission, User, UserActionLog, UserToken


@pytest.fixture
def client():
    app = create_app("testing")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_users()
            yield client
            db.session.remove()
            db.drop_all()


def seed_users():
    now = int(datetime.datetime.now().timestamp() * 1000)
    expires_at = now + 7 * 24 * 60 * 60 * 1000

    admin = User(
        id="admin-user-id",
        username="admin",
        name="管理员",
        password="x",
        role_id="admin",
        status=1,
        deleted=0,
        create_time=now,
    )
    user = User(
        id="normal-user-id",
        username="normal",
        name="普通用户",
        password="x",
        role_id="user",
        status=1,
        deleted=0,
        create_time=now,
    )
    admin_role = Role(
        id="admin",
        name="管理员",
        describe="拥有管理员权限",
        status=1,
        deleted=0,
        create_time=now,
    )
    user_role = Role(
        id="user",
        name="用户",
        describe="拥有用户权限",
        status=1,
        deleted=0,
        create_time=now,
    )
    admin_permission = RolePermission(
        id=1,
        role_id="admin",
        permission_id="admin",
        permission_name="管理员",
    )
    db.session.add_all(
        [
            admin,
            user,
            admin_role,
            user_role,
            admin_permission,
            UserToken(
                user_id=admin.id, token="admin-token", expires_at=expires_at
            ),  # noqa: E501
            UserToken(
                user_id=user.id, token="user-token", expires_at=expires_at
            ),  # noqa: E501
        ]
    )
    db.session.commit()


def test_authenticated_api_request_is_logged_and_admin_can_query(client):
    response = client.get("/api/users", headers={"Access-Token": "user-token"})
    assert response.status_code == 200

    query = client.get(
        "/api/audit/action-logs?userId=normal-user-id",
        headers={"Access-Token": "admin-token"},
    )
    assert query.status_code == 200

    data = json.loads(query.data)
    assert data["status"] == "success"
    assert data["pagination"]["total"] == 1
    assert data["logs"][0]["userId"] == "normal-user-id"
    assert data["logs"][0]["username"] == "normal"
    assert data["logs"][0]["actionType"] == "users.list"
    assert data["logs"][0]["method"] == "GET"
    assert data["logs"][0]["path"] == "/api/users"
    assert data["logs"][0]["statusCode"] == 200


def test_non_admin_cannot_query_action_logs(client):
    log = UserActionLog(
        user_id="normal-user-id",
        username="normal",
        name="普通用户",
        role_id="user",
        action_type="users.list",
        method="GET",
        path="/api/users",
        endpoint="users_user_list",
        status_code=200,
        client_ip="127.0.0.1",
        user_agent="pytest",
    )
    db.session.add(log)
    db.session.commit()

    response = client.get(
        "/api/audit/action-logs?userId=normal-user-id",
        headers={"Access-Token": "user-token"},
    )
    assert response.status_code == 403
