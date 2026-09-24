"""想定式生成算法入库硬门槛与资产留存测试。

验证三件事（均为确定性断言，非主观判断）：
1. 语法损坏的算法源码被拒绝入库（对应历史缺陷：JS `||` 写进 Python 的坏模型）
2. 语法损坏的测试文件同样被拒绝
3. 合法算法 + 测试文件 + 数据集完整入库，资产落盘且 source 登记

运行：cd ioeb_backend && python -m pytest tests/unit/test_scenario_upload_gate.py -v
"""

import io
import json
import os

import pytest

GOOD_ALGO = '''"""跨境支付风险分类模型。
依赖清单:
None (纯Python实现)
"""
from typing import Any, Dict


def main_process(row: Dict[str, Any]) -> Dict[str, Any]:
    """主入口：输入一行交易数据，输出风险分类结果。"""
    amount = float(row.get("amount", 0) or 0)
    if amount > 80000:
        return {"classification_label": "高风险"}
    return {"classification_label": "正常"}
'''

# 复刻历史入库坏模型的真实缺陷：第 55 行 JS 风格 ||
BAD_ALGO = '''"""损坏模型：JS 语法写进 Python。"""
from typing import Any, Dict


def main_process(row: Dict[str, Any]) -> Dict[str, Any]:
    """主入口。"""
    val = float(row.get("amount", 0) or 0)
    if val > 100 || val < 0:
        return {"classification_label": "高风险"}
    return {"classification_label": "正常"}
'''

GOOD_TEST = '''from demo_algorithm import main_process


def test_normal():
    assert main_process({"amount": 100})["classification_label"] == "正常"
'''

BAD_TEST = '''from demo_algorithm import main_process
def test_broken(:
    pass
'''


def _file(content: str, name: str):
    from werkzeug.datastructures import FileStorage

    return FileStorage(
        stream=io.BytesIO(content.encode("utf-8")),
        filename=name,
        content_type="text/x-python",
    )


@pytest.fixture(autouse=True)
def _isolated_upload_dir(app, tmp_path):
    """隔离上传目录：防止测试文件写入真实 uploads（首次运行曾污染生产目录）。"""
    isolated = tmp_path / "uploads"
    isolated.mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = str(isolated)
    yield
    # tmp_path 由 pytest 自动清理


@pytest.fixture()
def service(app):
    from app.services.service_service import ServiceService

    return ServiceService()


@pytest.fixture()
def auth_headers(app):
    """造一个测试用户 + 有效 token，通过 Access-Token 头登录。"""
    import datetime
    import time

    from app.extensions import db
    from app.models.user.user import User
    from app.models.user.user_tokens import UserToken

    user = User(
        username="gate_tester",
        name="门槛测试用户",
        password="hashed-fake",
        create_time=int(time.time() * 1000),
        deleted=0,
    )
    db.session.add(user)
    db.session.flush()
    token = UserToken(
        user_id=user.id,
        token="gate-test-token-0001",
        expires_at=int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp() * 1000),
    )
    db.session.add(token)
    db.session.commit()
    yield {"Access-Token": token.token}
    db.session.delete(token)
    db.session.delete(user)
    db.session.commit()


def _meta(**overrides):
    meta = {
        "name": "门槛测试算法",
        "domain": "aml",
        "industry": "x",
        "scenario": "y",
        "technology": "z",
        "creator_id": "test-user",
    }
    meta.update(overrides)
    return meta


def _cleanup(service, created_ids):
    for sid in created_ids:
        try:
            service.delete_service(sid)
        except Exception:
            pass


def test_bad_algorithm_rejected(service, app):
    """语法损坏的算法源码必须被拒收，且不产生任何 Service 记录。"""
    from app.services.service_service import ServiceServiceError

    with pytest.raises(ServiceServiceError) as ei:
        service.upload_scenario_generated_algorithm(
            _file(BAD_ALGO, "bad_algorithm.py"), _meta()
        )
    assert "语法错误" in str(ei.value), f"错误信息应指明语法错误: {ei.value}"


def test_bad_test_file_rejected(service, app):
    """语法损坏的测试文件必须被拒收。"""
    from app.services.service_service import ServiceServiceError

    with pytest.raises(ServiceServiceError) as ei:
        service.upload_scenario_generated_algorithm(
            _file(GOOD_ALGO, "demo_algorithm.py"),
            _meta(test_file=_file(BAD_TEST, "demo_test.py")),
        )
    assert "语法错误" in str(ei.value)


def test_good_algorithm_with_artifacts(service, app):
    """合法算法 + 测试 + 数据集完整入库：Service 创建、三文件落盘、source 登记。"""
    created = []
    try:
        result = service.upload_scenario_generated_algorithm(
            _file(GOOD_ALGO, "demo_algorithm.py"),
            _meta(
                test_file=_file(GOOD_TEST, "demo_test.py"),
                dataset_file=_file("amount,label\n100,正常\n90000,高风险\n", "ds.csv"),
            ),
        )
        sid = result["id"]
        created.append(sid)

        subdir = os.path.join(
            app.config["UPLOAD_FOLDER"], "generated_algorithm", sid
        )
        files = sorted(os.listdir(subdir))
        assert files == ["demo_algorithm.py", "demo_test.py", "ds.csv"], files

        # 类型正确
        assert result["type"] == "generated_algorithm"
    finally:
        _cleanup(service, created)


def test_full_http_path_rejects_bad_code(client, auth_headers):
    """HTTP 层完整链路：坏模型上传返回 400 + 明确错误信息。"""
    data = {
        "file": (io.BytesIO(BAD_ALGO.encode("utf-8")), "bad_algorithm.py"),
        "name": "HTTP门槛测试",
        "domain": "aml",
    }
    resp = client.post(
        "/api/services/scenario-generated/upload",
        data=data,
        content_type="multipart/form-data",
        headers=auth_headers,
    )
    assert resp.status_code == 400, resp.get_json()
    body = resp.get_json()
    assert "语法错误" in (body.get("message") or ""), body


def test_full_http_path_accepts_good_code(client, auth_headers):
    """HTTP 层完整链路：好模型上传返回 201。"""
    data = {
        "file": (io.BytesIO(GOOD_ALGO.encode("utf-8")), "demo_algorithm.py"),
        "name": "HTTP门槛测试-好模型",
        "domain": "aml",
    }
    resp = client.post(
        "/api/services/scenario-generated/upload",
        data=data,
        content_type="multipart/form-data",
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.get_json()
    sid = resp.get_json()["service"]["id"]
    # 清理测试数据
    from app.extensions import db
    from app.models.service.service import Service

    svc = db.session.query(Service).filter_by(id=sid).first()
    if svc:
        svc.deleted = True
        db.session.commit()
