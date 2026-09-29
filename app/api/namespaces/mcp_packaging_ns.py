"""Authenticated MCP packaging workflow for the standalone factory site."""

import ast
import base64
import hashlib
import io
import json
import os
import re
import stat
from pathlib import Path
import threading
import time
import uuid
import zipfile

import requests
import yaml
from flask import current_app, request, send_file
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.mcp_packaging_job import McpPackagingJob
from app.services.service_service import ServiceServiceError, service_service
from app.utils.auth_utils import get_request_user


api = Namespace("mcp-packaging", description="MCP 想定式封装")
MAX_SOURCE_BYTES = 15 * 1024 * 1024
MAX_PACKAGE_BYTES = 100 * 1024 * 1024
RUNNING = {"packaging", "deploying"}


def _now():
    return int(time.time() * 1000)


def _root():
    root = Path(os.environ.get("MCP_PACKAGING_BASE_PATH") or Path(current_app.config["UPLOAD_FOLDER"]) / "mcp-packaging")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _job(job_id, user):
    job = McpPackagingJob.query.filter_by(id=job_id, owner_id=user.id).first()
    if job is None:
        api.abort(404, "封装任务不存在")
    return job


def _service_state(job):
    if not job.service_id:
        return None
    from app.models.service.service import Service
    service = db.session.get(Service, job.service_id)
    return service.status if service else "missing"


def _login():
    user = get_request_user()
    if user is None:
        api.abort(401, "请先登录")
    return user


def _save(job, **values):
    for key, value in values.items():
        setattr(job, key, value)
    job.updated_at = _now()
    db.session.commit()
    return job


def _candidate_functions(path):
    """Static suggestions only; parsing source never executes uploaded code."""
    sources = []
    if path.suffix.lower() == ".py":
        sources = [(path.name, path.read_bytes())]
    else:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                name = info.filename.replace("\\", "/")
                if (name.startswith("/") or ".." in Path(name).parts or info.file_size > 1024 * 1024
                        or info.is_dir()):
                    continue
                if name.endswith(".py") and name.count("/") <= 3:
                    sources.append((name, archive.read(info)))
                if len(sources) >= 30:
                    break
    result = []
    for filename, raw in sources:
        try:
            tree = ast.parse(raw.decode("utf-8-sig"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                params = [arg.arg for arg in node.args.args if arg.arg not in {"self", "cls"}]
                result.append({"entrypoint": f"{filename}:{node.name}", "name": node.name,
                               "description": (ast.get_docstring(node) or "")[:500],
                               "parameters": params})
    return result[:100]


def _validate_package(package):
    """Constrain generated Compose before giving it to the Docker-enabled backend."""
    with zipfile.ZipFile(io.BytesIO(package)) as archive:
        files = {}
        for item in archive.infolist():
            name = item.filename.replace("\\", "/")
            if name.startswith("/") or ".." in Path(name).parts or re.match(r"^[A-Za-z]:", name):
                raise ValueError("封装包包含不安全路径")
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("封装包不能包含符号链接")
            if item.file_size > MAX_PACKAGE_BYTES:
                raise ValueError("封装包包含过大文件")
            if not item.is_dir():
                files[Path(name).name] = item
        if len(files) > 500 or sum(item.file_size for item in files.values()) > 200 * 1024 * 1024:
            raise ValueError("封装包内容过大")
        if not {"server.py", "Dockerfile", "docker-compose.yml"} <= files.keys():
            raise ValueError("封装包缺少部署文件")
        config = yaml.safe_load(archive.read(files["docker-compose.yml"]))
        services = config.get("services") if isinstance(config, dict) else None
        if not isinstance(services, dict) or len(services) != 1:
            raise ValueError("封装包必须只包含一个服务")
        service = next(iter(services.values()))
        if not isinstance(service, dict):
            raise ValueError("Compose 服务配置无效")
        forbidden = {"privileged", "volumes", "devices", "cap_add", "security_opt", "pid",
                     "ipc", "network_mode", "userns_mode", "extra_hosts", "env_file", "secrets"}
        if forbidden & service.keys():
            raise ValueError("封装包请求了不允许的容器权限或宿主机挂载")
        ports = service.get("ports")
        if not isinstance(ports, list) or len(ports) != 1:
            raise ValueError("MCP 服务必须只声明一个端口")
        build = service.get("build")
        if build != "." and not (isinstance(build, dict) and build.get("context") == "."):
            raise ValueError("只能从封装包当前目录构建镜像")


def _agent_package(source_path, spec, on_progress):
    endpoint = os.environ.get("MCP_AGENT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    with open(source_path, "rb") as source:
        response = requests.post(
            endpoint + "/api/agent/service_packaging",
            files={"file": (source_path.name, source, "application/octet-stream")},
            data={"packaging_spec": json.dumps(spec, ensure_ascii=False)},
            stream=True, timeout=(15, 1200),
        )
        response.raise_for_status()
        task_id = response.headers.get("X-Task-ID")
        on_progress(task_id, "Agent 已接收封装任务")
        result = None
        error = None
        for line in response.iter_lines(decode_unicode=True):
            if isinstance(line, bytes):
                line = line.decode("utf-8", errors="replace")
            if not line or not line.startswith("data:"):
                continue
            event = json.loads(line[5:].strip())
            step = event.get("step")
            if step is not None:
                on_progress(task_id, f"正在处理第 {step} 步")
            if event.get("error"):
                error = str(event["error"])
            if event.get("is_final_result"):
                result = (event.get("final_results") or {}).get("service_package")
                error = event.get("error") or (event.get("final_results") or {}).get("error") or error
        response.close()
    if error or not result or not result.get("content"):
        raise ValueError(error or "Agent 未返回完整封装包")
    package = base64.b64decode(result["content"], validate=True)
    if len(package) > MAX_PACKAGE_BYTES:
        raise ValueError("封装包超过 100 MB")
    _validate_package(package)
    return package


def _package_worker(app, job_id, revision):
    with app.app_context():
        job = db.session.get(McpPackagingJob, job_id)
        if job is None:
            return
        try:
            def progress(task_id, message):
                current = db.session.get(McpPackagingJob, job_id)
                if current and current.status in {"packaging", "cancelling"}:
                    _save(current, agent_task_id=task_id, progress_text=message[:500])
                    if current.status == "cancelling":
                        if task_id:
                            endpoint = os.environ.get("MCP_AGENT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
                            requests.post(f"{endpoint}/api/tasks/{task_id}/cancel", timeout=10)
                        raise ValueError("用户已取消封装")

            package = _agent_package(Path(job.source_path), json.loads(job.spec_json), progress)
            job = db.session.get(McpPackagingJob, job_id)
            if job.revision != revision or job.status != "packaging":
                return
            path = _root() / job.id / "package.zip"
            path.write_bytes(package)
            _save(job, status="packaged", stage="package", artifact_path=str(path),
                  artifact_digest=hashlib.sha256(package).hexdigest(), error=None)
        except Exception as exc:
            app.logger.exception("MCP packaging failed: %s", job_id)
            job = db.session.get(McpPackagingJob, job_id)
            if job and job.status in {"packaging", "cancelling"}:
                _save(job, status="cancelled" if job.status == "cancelling" else "failed",
                      error=None if job.status == "cancelling" else str(exc)[:1000])


@api.route("/jobs")
class Jobs(Resource):
    def get(self):
        user = _login()
        jobs = McpPackagingJob.query.filter_by(owner_id=user.id).order_by(McpPackagingJob.updated_at.desc()).limit(100).all()
        return {"jobs": [job.snapshot() for job in jobs]}

    def post(self):
        user = _login()
        data = request.get_json(silent=True) or {}
        service_id = data.get("sourceServiceId")
        job_id = str(uuid.uuid4())
        path = ""
        source_name = ""
        digest = ""
        if service_id:
            from app.models.service.service import Service
            source = db.session.get(Service, str(service_id))
            if not source or source.deleted or source.type != "generated_algorithm" or source.status == "draft":
                api.abort(404, "算法不存在")
            if str(source.creator_id) != str(user.id):
                api.abort(403, "无权读取算法源码")
            try:
                path, source_name = service_service.get_scenario_generated_code_path(str(service_id))
            except ServiceServiceError as exc:
                api.abort(400, str(exc))
            digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        job = McpPackagingJob(id=job_id, owner_id=user.id, source_service_id=service_id,
                              source_path=path, source_name=source_name, source_digest=digest)
        if path:
            candidates = _candidate_functions(Path(path))
            if not candidates:
                api.abort(400, "该算法源码没有可封装的 Python 函数")
            job.candidates_json = json.dumps(candidates, ensure_ascii=False)
            job.stage = "intent"
        db.session.add(job)
        db.session.commit()
        return {"job": job.snapshot()}, 201


@api.route("/jobs/<string:job_id>")
class Job(Resource):
    def get(self, job_id):
        job = _job(job_id, _login())
        if job.status in {"packaging", "cancelling"} and _now() - job.updated_at > 45 * 60 * 1000:
            _save(job, status="interrupted", error="任务长时间没有进度，请重试")
        if job.status == "deploying" and not job.service_id and _now() - job.updated_at > 5 * 60 * 1000:
            _save(job, status="interrupted", error="部署登记中断，请联系管理员核对服务记录")
        return {"job": {**job.snapshot(), "serviceStatus": _service_state(job)}}

    def patch(self, job_id):
        job = _job(job_id, _login())
        data = request.get_json(silent=True) or {}
        if job.status in RUNNING or job.status == "cancelling" or job.service_id:
            api.abort(409, "任务正在运行或已部署")
        if data.get("revision") != job.revision:
            api.abort(409, "草稿已更新，请刷新")
        spec = data.get("spec")
        if not isinstance(spec, dict):
            api.abort(400, "缺少封装想定")
        candidates = {item["entrypoint"] for item in json.loads(job.candidates_json)}
        tools = spec.get("tools")
        if not isinstance(tools, list) or not tools or len(tools) > 20:
            api.abort(400, "请选择 1 到 20 个工具")
        if any(not isinstance(tool, dict) or tool.get("entrypoint") not in candidates for tool in tools):
            api.abort(400, "工具必须来自当前源码分析结果")
        names = [tool.get("name") for tool in tools]
        if any(not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", name) for name in names) or len(set(names)) != len(names):
            api.abort(400, "工具名须唯一，且只包含英文字母、数字和下划线")
        if any(not isinstance(tool.get("input_schema"), dict) or tool["input_schema"].get("type") != "object" for tool in tools):
            api.abort(400, "每个工具必须提供对象类型的输入 Schema")
        for tool in tools:
            schema = tool["input_schema"]
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            if (not isinstance(properties, dict) or any(not isinstance(value, dict) for value in properties.values())
                    or not isinstance(required, list) or any(key not in properties for key in required)):
                api.abort(400, "工具输入 Schema 的 properties 或 required 无效")
        if not str(spec.get("service_name") or "").strip() or not str(spec.get("scenario") or "").strip():
            api.abort(400, "请填写名称和使用场景")
        spec["source_digest"] = job.source_digest
        spec["transport"] = "sse"
        _save(job, spec_json=json.dumps(spec, ensure_ascii=False), revision=job.revision + 1,
              artifact_path=None, artifact_digest=None, verified_tools_json="[]",
              verified_at=None, status="draft", stage="intent", error=None)
        return {"job": job.snapshot()}


@api.route("/jobs/<string:job_id>/source")
class JobSource(Resource):
    def put(self, job_id):
        job = _job(job_id, _login())
        if job.source_service_id or job.status in RUNNING or job.status == "cancelling" or job.service_id:
            api.abort(409, "此任务不能更换来源")
        upload = request.files.get("file")
        if not upload or not upload.filename or Path(upload.filename).suffix.lower() not in {".py", ".zip"}:
            api.abort(400, "仅支持 .py 或 .zip")
        raw = upload.read(MAX_SOURCE_BYTES + 1)
        if not raw or len(raw) > MAX_SOURCE_BYTES:
            api.abort(400, "源码文件为空或超过 15 MB")
        if upload.filename.lower().endswith(".zip") and not zipfile.is_zipfile(io.BytesIO(raw)):
            api.abort(400, "ZIP 格式无效")
        directory = _root() / job.id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / ("source" + Path(upload.filename).suffix.lower())
        path.write_bytes(raw)
        candidates = _candidate_functions(path)
        if not candidates:
            path.unlink(missing_ok=True)
            api.abort(400, "未发现可封装的 Python 函数")
        _save(job, source_path=str(path), source_name=secure_filename(upload.filename),
              source_digest=hashlib.sha256(raw).hexdigest(),
              candidates_json=json.dumps(candidates, ensure_ascii=False), spec_json="{}",
              revision=job.revision + 1, artifact_path=None, artifact_digest=None,
              verified_tools_json="[]", verified_at=None,
              status="draft", stage="intent", error=None)
        return {"job": job.snapshot()}


@api.route("/jobs/<string:job_id>/intake")
class JobIntake(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if not job.source_path or job.service_id:
            api.abort(409, "请先选择源码")
        data = request.get_json(silent=True) or {}
        message = str(data.get("message") or "").strip()
        if not message or len(message) > 4000:
            api.abort(400, "请输入 1 至 4000 字想定描述")
        endpoint = os.environ.get("MCP_AGENT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
        try:
            response = requests.post(endpoint + "/api/agent/mcp_packaging_intake",
                data={"message": message, "partial_form": json.dumps(data.get("partialForm") or {}, ensure_ascii=False),
                      "candidates": job.candidates_json}, timeout=90)
            response.raise_for_status()
            result = response.json()
            if not isinstance(result.get("updates"), dict):
                raise ValueError("想定返回格式无效")
            return result
        except (requests.RequestException, ValueError) as exc:
            return {"status": "error", "message": f"想定助手暂不可用: {exc}"}, 502


@api.route("/jobs/<string:job_id>/package")
class JobPackage(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.status == "packaging":
            return {"job": job.snapshot()}, 202
        if job.status not in {"draft", "failed", "interrupted", "cancelled", "packaged"} or not job.source_path:
            api.abort(409, "请先完成来源和想定")
        spec = json.loads(job.spec_json)
        if not spec.get("tools"):
            api.abort(400, "请先确认工具")
        if not Path(job.source_path).is_file() or hashlib.sha256(Path(job.source_path).read_bytes()).hexdigest() != job.source_digest:
            api.abort(409, "源码已变化，请重新创建任务")
        _save(job, status="packaging", stage="package", error=None, artifact_path=None,
              agent_task_id=None, progress_text="等待 Agent 接收")
        threading.Thread(target=_package_worker,
                         args=(current_app._get_current_object(), job.id, job.revision),
                         daemon=True).start()
        return {"job": job.snapshot()}, 202


@api.route("/jobs/<string:job_id>/cancel")
class JobCancel(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.status not in {"packaging", "cancelling"}:
            api.abort(409, "当前没有可取消的生成任务")
        _save(job, status="cancelling", progress_text="正在取消")
        if job.agent_task_id:
            endpoint = os.environ.get("MCP_AGENT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
            try:
                requests.post(f"{endpoint}/api/tasks/{job.agent_task_id}/cancel", timeout=10)
            except requests.RequestException:
                pass
        return {"job": job.snapshot()}, 202


@api.route("/jobs/<string:job_id>/artifact")
class JobArtifact(Resource):
    def get(self, job_id):
        job = _job(job_id, _login())
        if job.status not in {"packaged", "deploying", "deployed"} or not job.artifact_path or not Path(job.artifact_path).is_file():
            api.abort(404, "封装包尚未生成")
        return send_file(job.artifact_path, as_attachment=True, download_name="mcp-service-package.zip")


@api.route("/jobs/<string:job_id>/deploy")
class JobDeploy(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.service_id:
            return {"job": job.snapshot(), "serviceId": job.service_id}
        if job.status != "packaged" or not job.artifact_path:
            api.abort(409, "请先生成封装包")
        try:
            _validate_package(Path(job.artifact_path).read_bytes())
        except (OSError, ValueError, zipfile.BadZipFile, yaml.YAMLError) as exc:
            api.abort(400, f"封装包校验失败: {exc}")
        spec = json.loads(job.spec_json)
        claimed = McpPackagingJob.query.filter_by(id=job.id, owner_id=job.owner_id,
                                                   status="packaged", service_id=None).update(
            {"status": "deploying", "updated_at": _now()}, synchronize_session=False)
        db.session.commit()
        if claimed != 1:
            api.abort(409, "部署已在进行，请刷新状态")
        try:
            with open(job.artifact_path, "rb") as stream:
                uploaded = FileStorage(stream=stream, filename="mcp-service-package.zip", content_type="application/zip")
                service = service_service.upload_and_deploy_service(uploaded, {
                    "name": spec["service_name"][:100], "creator_id": job.owner_id,
                    "type": "atomic_mcp", "domain": str(spec.get("domain") or "aml")[:50],
                    "scenario": str(spec.get("scenario") or "")[:50],
                    "technology": "MCP", "attribute": "non_intelligent",
                    "suppress_placeholder_tools": True,
                })
        except Exception as exc:
            db.session.expire_all()
            _save(job, status="packaged", error=str(exc)[:1000])
            return {"status": "error", "message": str(exc)}, 400
        service_id = service.get("id")
        db.session.expire_all()
        _save(job, status="deploying", stage="deploy", service_id=service_id)
        return {"job": job.snapshot(), "serviceId": service_id}, 202


@api.route("/jobs/<string:job_id>/check")
class JobCheck(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        state = _service_state(job)
        if state not in {"pre_release_unrated", "pre_release_pending", "released"}:
            api.abort(409, "服务尚未完成部署")
        from app.models.service.service import Service
        service = db.session.get(Service, job.service_id)
        if not service.apis or not service.apis[0].url:
            api.abort(409, "服务缺少 MCP 接入地址")
        host_port = str(service.port or "").split(",")[0].split(":")[0]
        expected_url = (os.environ.get("SERVICE_HOST_URL", "https://fdueblab.cn").rstrip("/")
                        + f"/mcp-proxy/{host_port}/sse")
        if not host_port.isdigit() or service.apis[0].url != expected_url:
            api.abort(409, "服务接入地址与平台部署记录不一致")
        secret = os.environ.get("MCP_INTERNAL_TOKEN", "")
        if not secret:
            api.abort(503, "MCP 内部验证未配置")
        endpoint = os.environ.get("MCP_AGENT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
        data = request.get_json(silent=True) or {}
        tool_name = data.get("toolName")
        arguments = data.get("arguments") or {}
        if tool_name and (not isinstance(tool_name, str) or not isinstance(arguments, dict)):
            api.abort(400, "工具调用参数无效")
        if tool_name and data.get("confirmCall") is not True:
            api.abort(400, "请确认执行本次工具调用")
        try:
            response = requests.post(endpoint + "/api/internal/mcp/check",
                headers={"X-MCP-Internal-Token": secret},
                json={"server_url": service.apis[0].url, "transport": service.apis[0].method,
                      "tool_name": tool_name, "arguments": arguments}, timeout=60)
            response.raise_for_status()
            result = response.json()
        except (requests.RequestException, ValueError) as exc:
            return {"status": "error", "message": f"MCP 验证失败: {exc}"}, 502
        tools = result.get("tools") or []
        expected = {item.get("name") for item in json.loads(job.spec_json).get("tools", [])}
        actual = {item.get("name") for item in tools}
        if expected != actual:
            return {"status": "error", "message": "实际工具清单与确认的封装想定不一致",
                    "missingTools": sorted(expected - actual), "unexpectedTools": sorted(actual - expected), "tools": tools}, 422
        for expected_tool in json.loads(job.spec_json).get("tools", []):
            actual_tool = next(item for item in tools if item["name"] == expected_tool["name"])
            expected_schema = expected_tool["input_schema"]
            actual_schema = actual_tool.get("inputSchema") or {}
            expected_properties = expected_schema.get("properties", {})
            actual_properties = actual_schema.get("properties", {})
            schema_differs = (set(expected_properties) != set(actual_properties)
                              or set(expected_schema.get("required", [])) != set(actual_schema.get("required", []))
                              or any(expected_properties[key].get("type") != actual_properties[key].get("type")
                                     for key in set(expected_properties) & set(actual_properties)))
            if schema_differs:
                return {"status": "error", "message": f"工具 {expected_tool['name']} 的实际参数与想定不一致",
                        "tools": tools}, 422
        # Replace placeholder tools created by the legacy upload path.
        if not job.verified_at:
            service_service.service_repository.update_service_with_relations(job.service_id, {
            "apiList": [{"name": service.apis[0].name, "url": service.apis[0].url,
                         "method": service.apis[0].method, "des": service.apis[0].des,
                         "parameterType": 1, "responseType": 1,
                         "tools": [{"name": item["name"], "description": item.get("description", "")}
                                   for item in tools]}]
            })
        _save(job, status="deployed", stage="check", verified_tools_json=json.dumps(tools, ensure_ascii=False),
              verified_at=_now())
        return {"status": "success", "tools": tools, "call": result.get("call"),
                "job": {**job.snapshot(), "serviceStatus": _service_state(job)}}


@api.route("/jobs/<string:job_id>/submit-review")
class JobSubmitReview(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if not job.verified_at or not job.service_id:
            api.abort(409, "请先通过 MCP 协议和工具校验")
        state = _service_state(job)
        if state == "pre_release_pending":
            return {"job": {**job.snapshot(), "serviceStatus": state}}
        if state != "pre_release_unrated":
            api.abort(409, "当前部署状态不能提交审核")
        service_service.service_repository.update_service_status(job.service_id, "pre_release_pending")
        return {"job": {**job.snapshot(), "serviceStatus": "pre_release_pending"}}
