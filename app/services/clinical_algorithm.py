"""Validated, isolated execution of clinical algorithm source files."""

import ast
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess

from flask import current_app

from app.extensions import db
from app.models.service.algorithm_artifact import AlgorithmArtifact
from app.models.service.service import Service


class ClinicalAlgorithmError(ValueError):
    pass


_TYPES = {"number", "integer", "string", "boolean"}
_RUNNER = """import contextlib, importlib.util, json, os, sys
with contextlib.redirect_stdout(sys.stderr):
    spec = importlib.util.spec_from_file_location('clinical_algorithm', os.environ['CLINICAL_MODEL_PATH'])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.main_process(**json.load(sys.stdin))
encoded = json.dumps(result, ensure_ascii=False, allow_nan=False)
if len(encoded.encode('utf-8')) > 65536:
    raise ValueError('模型输出超过 64 KB')
print(encoded)
"""


def normalize_spec(spec, source_code):
    """Check the UI contract against the actual main_process signature."""
    if not isinstance(spec, dict) or not isinstance(spec.get("inputs"), list):
        raise ClinicalAlgorithmError("缺少结构化输入规范")
    if not 1 <= len(spec["inputs"]) <= 30:
        raise ClinicalAlgorithmError("输入字段数量必须在 1 至 30 之间")
    names = []
    clean_inputs = []
    for item in spec["inputs"]:
        if not isinstance(item, dict):
            raise ClinicalAlgorithmError("输入字段格式错误")
        name, kind = item.get("name"), item.get("type")
        if not isinstance(name, str) or not name.isidentifier() or name.startswith("_"):
            raise ClinicalAlgorithmError("输入字段名称无效")
        if name in names or kind not in _TYPES:
            raise ClinicalAlgorithmError("输入字段重复或类型不受支持")
        names.append(name)
        options = item.get("options") if kind == "string" else None
        if options is not None and (not isinstance(options, list) or len(options) > 100 or
                                    any(not isinstance(option, str) or len(option) > 200 for option in options)):
            raise ClinicalAlgorithmError("选项必须是至多 100 个短文本值")
        minimum, maximum = item.get("minimum"), item.get("maximum")
        if minimum is not None or maximum is not None:
            if kind not in ("number", "integer") or any(
                value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value))
                for value in (minimum, maximum)
            ) or (minimum is not None and maximum is not None and minimum > maximum):
                raise ClinicalAlgorithmError("输入字段的数值范围无效")
        clean_inputs.append({
            "name": name, "type": kind,
            "label": str(item.get("label") or name)[:100],
            "unit": str(item.get("unit") or "")[:30],
            "description": str(item.get("description") or "")[:300],
            "required": item.get("required") is not False,
            "options": options or [],
            "minimum": minimum,
            "maximum": maximum,
        })
    tree = ast.parse(source_code)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "main_process"]
    if len(functions) != 1 or isinstance(functions[0], ast.AsyncFunctionDef):
        raise ClinicalAlgorithmError("代码需要一个同步的 main_process 入口")
    args = functions[0].args
    if args.vararg or args.kwarg or args.posonlyargs or args.kwonlyargs:
        raise ClinicalAlgorithmError("main_process 必须使用明确命名的参数")
    if names != [arg.arg for arg in args.args]:
        raise ClinicalAlgorithmError("输入规范与 main_process 参数不一致")
    return {
        "title": str(spec.get("title") or "临床算法")[:100],
        "description": str(spec.get("description") or "")[:500],
        "clinicalScope": str(spec.get("clinicalScope") or "")[:500],
        "inputs": clean_inputs,
        "output": spec.get("output") if isinstance(spec.get("output"), dict) else {},
    }


def validate_input(spec, values):
    try:
        serialized = json.dumps(values, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ClinicalAlgorithmError("输入必须是有限的 JSON 数据") from exc
    if not isinstance(values, dict) or len(serialized) > 16384:
        raise ClinicalAlgorithmError("输入需要是大小不超过 16 KB 的对象")
    expected = {item["name"]: item for item in spec["inputs"]}
    if set(values) - set(expected):
        raise ClinicalAlgorithmError("输入包含未定义字段")
    clean = {}
    for name, field in expected.items():
        if name not in values or values[name] is None:
            if field["required"]:
                raise ClinicalAlgorithmError(f"缺少必填字段：{field['label']}")
            continue
        value, kind = values[name], field["type"]
        valid = (
            (kind == "number" and isinstance(value, (int, float)) and not isinstance(value, bool))
            or (kind == "integer" and isinstance(value, int) and not isinstance(value, bool))
            or (kind == "string" and isinstance(value, str) and len(value) <= 4000)
            or (kind == "boolean" and isinstance(value, bool))
        )
        if not valid:
            raise ClinicalAlgorithmError(f"字段类型无效：{field['label']}")
        if kind in ("number", "integer") and not math.isfinite(value):
            raise ClinicalAlgorithmError(f"数值必须有限：{field['label']}")
        if kind in ("number", "integer") and ((field.get("minimum") is not None and value < field["minimum"]) or (field.get("maximum") is not None and value > field["maximum"])):
            raise ClinicalAlgorithmError(f"数值超出允许范围：{field['label']}")
        if kind == "string" and field["options"] and value not in field["options"]:
            raise ClinicalAlgorithmError(f"字段选项无效：{field['label']}")
        clean[name] = value
    return clean


def validate_units(spec, units):
    if not isinstance(units, dict):
        raise ClinicalAlgorithmError("缺少输入单位信息")
    expected = {item["name"]: item["unit"] for item in spec["inputs"] if item.get("unit")}
    for name, unit in expected.items():
        if units.get(name) != unit:
            raise ClinicalAlgorithmError(f"字段单位不一致：{name}，需要 {unit}")


def compare_reference_output(actual, expected, absolute_tolerance, relative_tolerance):
    """Compare a real model result with an independently supplied reference result."""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual is expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isfinite(actual) and math.isfinite(expected) and math.isclose(
            actual, expected, abs_tol=absolute_tolerance, rel_tol=relative_tolerance,
        )
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            compare_reference_output(actual[key], expected[key], absolute_tolerance, relative_tolerance)
            for key in expected
        )
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(
            compare_reference_output(left, right, absolute_tolerance, relative_tolerance)
            for left, right in zip(actual, expected)
        )
    return type(actual) is type(expected) and actual == expected


def run_isolated(code_path, inputs):
    """Run untrusted model code in a resource-limited container."""
    code_path = Path(code_path).resolve()
    upload_root = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
    relative = code_path.relative_to(upload_root)
    host_root = Path(os.environ.get("CLINICAL_UPLOADS_HOST_PATH") or str(upload_root)).resolve()
    host_code_path = host_root / relative
    image = os.environ.get("CLINICAL_RUNNER_IMAGE", "python:3.12-slim")
    volume_name = os.environ.get("CLINICAL_UPLOADS_DOCKER_VOLUME", "").strip()
    if volume_name:
        mount = f"type=volume,source={volume_name},target=/algorithm/uploads,readonly"
        model_path = "/algorithm/uploads/" + relative.as_posix()
    else:
        mount = f"type=bind,source={host_code_path},target=/algorithm/model.py,readonly"
        model_path = "/algorithm/model.py"
    from uuid import uuid4
    container_name = f"zzf-clinical-{uuid4().hex}"
    cmd = [
        "docker", "run", "--rm", "--name", container_name, "--pull", "never", "--interactive", "--network", "none",
        "--read-only", "--memory", "256m", "--cpus", "1", "--pids-limit", "64",
        "--security-opt", "no-new-privileges", "--cap-drop", "ALL",
        "--user", "65534:65534", "--mount", mount,
        "--env", f"CLINICAL_MODEL_PATH={model_path}",
        image, "python", "-B", "-c", _RUNNER,
    ]
    try:
        proc = subprocess.run(
            cmd, input=json.dumps(inputs, ensure_ascii=False), text=True,
            capture_output=True, timeout=20, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
        raise ClinicalAlgorithmError("模型运行超时") from exc
    except OSError as exc:
        raise ClinicalAlgorithmError(f"受控运行环境不可用：{type(exc).__name__}") from exc
    if proc.returncode:
        raise ClinicalAlgorithmError("模型运行失败；请检查输入、依赖和代码")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ClinicalAlgorithmError("模型输出不是 JSON 数据") from exc


def _source_with_validation(source, status, reason=None):
    updated = dict(source) if isinstance(source, dict) else {}
    submitted_lines = updated.get("generationEvidence")
    lines = [str(line)[:1000] for line in submitted_lines[:20]] if isinstance(submitted_lines, list) else []
    if status == "ready":
        statement = "验证：平台样例运行已通过；业务效果仍需独立数据集评估。"
    elif status == "needs_configuration":
        statement = f"验证：尚未执行平台样例运行；{reason or '缺少在线运行配置'}。"
    else:
        statement = f"验证：平台样例运行未通过；{reason or '尚未满足在线运行条件'}。"
    while len(lines) < 3:
        lines.append("")
    lines[2] = statement
    updated["generationEvidence"] = lines
    updated["platformValidation"] = {"status": status, "reason": reason}
    return json.dumps(updated, ensure_ascii=False)


def create_artifact(service_id, code_path, spec, smoke_input, source=None):
    source_code = Path(code_path).read_text(encoding="utf-8")
    normalized = normalize_spec(spec, source_code)
    smoke = validate_input(normalized, smoke_input)
    artifact = AlgorithmArtifact(
        service_id=service_id, version=1,
        code_sha256=hashlib.sha256(Path(code_path).read_bytes()).hexdigest(),
        spec_json=json.dumps(normalized, ensure_ascii=False),
        smoke_input_json=json.dumps(smoke, ensure_ascii=False),
        source_json=json.dumps(source or {}, ensure_ascii=False),
    )
    db.session.add(artifact)
    db.session.commit()
    try:
        run_isolated(code_path, smoke)
        artifact.mark_ready()
    except ClinicalAlgorithmError as exc:
        artifact.status = "draft"
        artifact.validation_error = str(exc)
    artifact.source_json = _source_with_validation(source, artifact.status, artifact.validation_error)
    db.session.commit()
    return artifact


def create_unconfigured_artifact(service_id, code_path, source=None, reason=None):
    """Keep the generated model and its provenance visible until a runnable contract exists."""
    artifact = AlgorithmArtifact(
        service_id=service_id,
        version=1,
        code_sha256=hashlib.sha256(Path(code_path).read_bytes()).hexdigest(),
        spec_json=json.dumps({"title": "待配置算法", "description": "尚未提供可验证的输入规范", "inputs": [], "output": {}}, ensure_ascii=False),
        status="needs_configuration",
        validation_error=reason or "缺少可验证的输入规范或运行样例",
        source_json=_source_with_validation(source, "needs_configuration", reason or "缺少可验证的输入规范或运行样例"),
    )
    db.session.add(artifact)
    db.session.commit()
    return artifact


def configure_artifact(service_id, code_path, spec, smoke_input):
    """Revalidate an existing artifact when its author supplies a runnable contract."""
    artifact = get_artifact(service_id)
    source_code = Path(code_path).read_text(encoding="utf-8")
    normalized = normalize_spec(spec, source_code)
    smoke = validate_input(normalized, smoke_input)
    source = json.loads(artifact.source_json or "{}")
    source.pop("referenceCheck", None)
    artifact.version += 1
    artifact.code_sha256 = hashlib.sha256(Path(code_path).read_bytes()).hexdigest()
    artifact.spec_json = json.dumps(normalized, ensure_ascii=False)
    artifact.smoke_input_json = json.dumps(smoke, ensure_ascii=False)
    artifact.status = "draft"
    artifact.validation_error = None
    artifact.validated_at = None
    source["publicTrialEnabled"] = False
    db.session.commit()
    try:
        run_isolated(code_path, smoke)
        artifact.mark_ready()
    except ClinicalAlgorithmError as exc:
        artifact.validation_error = str(exc)
    artifact.source_json = _source_with_validation(source, artifact.status, artifact.validation_error)
    db.session.commit()
    return artifact


def get_artifact(service_id):
    service = Service.query.filter_by(id=service_id, type="generated_algorithm", deleted=0).first()
    if not service:
        raise ClinicalAlgorithmError("算法模型不存在")
    artifact = AlgorithmArtifact.query.filter_by(service_id=service_id).first()
    if not artifact:
        raise ClinicalAlgorithmError("该算法尚未配置在线使用")
    return artifact


def verify_artifact_code(artifact, code_path):
    """Reject edits to a source file after its smoke test."""
    try:
        actual = hashlib.sha256(Path(code_path).read_bytes()).hexdigest()
    except OSError as exc:
        raise ClinicalAlgorithmError("模型源码无法读取") from exc
    if actual != artifact.code_sha256:
        raise ClinicalAlgorithmError("模型源码与验证版本不一致，请重新登记并验证")
