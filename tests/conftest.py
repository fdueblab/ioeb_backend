import os
import tempfile

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    """创建应用实例"""
    app = create_app("testing")

    # 配置测试环境
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    # 创建上下文
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """创建测试客户端"""
    with app.test_client() as client:
        yield client
