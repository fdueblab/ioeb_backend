"""Minimal clinical model creation with durable drafts and generation progress."""

import io
import json
import os
import threading
import time
import uuid
from contextlib import ExitStack
from pathlib import Path

import requests
from flask import current_app, request, send_file
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.clinical_creation_job import ClinicalCreationJob
from app.services.service_service import ServiceServiceError, service_service
from app.utils.auth_utils import get_request_user


api = Namespace("clinical-creation", description="临床算法创建任务")
from app.services.clinical_catalog import public_catalog, department, paper, attach_paper, has_materials
MAX_REFERENCE_BYTES = 10 * 1024 * 1024
MAX_RESULT_BYTES = 2 * 1024 * 1024
STALE_AFTER_MS = 30000


def _now():
    return int(time.time() * 1000)


def _agent_url():
    return (os.environ.get("CLINICAL_AGENT_BASE_URL") or
            os.environ.get("MCP_AGENT_BASE_URL") or "http://127.0.0.1:8010").rstrip("/")


def _login():
    user = get_request_user()
    if user is None:
        api.abort(401, "请先登录")
    return user


def _job(job_id, user):
    job = ClinicalCreationJob.query.filter_by(id=job_id, owner_id=str(user.id)).first()
    if job is None:
        api.abort(404, "创建任务不存在")
    if job.status == "running" and _now() - (job.heartbeat_at or job.updated_at) > STALE_AFTER_MS:
        # A stale local heartbeat is not evidence that the remote task stopped.
        job.progress_text = "正在确认任务状态，请勿重复提交"
        execution = json.loads(job.intake_json or "{}").get("execution") or {}
        if execution.get("run_id") == job.run_id and execution.get("resume_token"):
            try:
                reply = requests.get(_agent_url() + "/api/agent/clinical-runs/" + execution["resume_token"], timeout=(2, 3))
                reply.raise_for_status()
                delivery = reply.json()
                result = delivery.get("result")
                if delivery.get("status") == "completed" and isinstance(result, dict):
                    from app.services.clinical_reproduction import reproduction_gaps
                    gaps = reproduction_gaps(result)
                    if not gaps and result.get("reproduction", {}).get("status") == "pending_runtime":
                        try:
                            from app.services.clinical_reproduction import verify_candidate
                            verify_candidate(result, _reference_folder(job) / job.run_id)
                        except Exception as exc:
                            gaps = ["平台运行验证未通过：" + str(exc)[:500]]
                    if not result.get("generated_code") and not gaps:
                        gaps = ["生成结果缺少算法代码"]
                    encoded = json.dumps(result, ensure_ascii=False)
                    if len(encoded.encode("utf-8")) <= MAX_RESULT_BYTES:
                        return _save(job, status="needs_review" if gaps else "completed", result_json=encoded,
                                     error="；".join(gaps) if gaps else None, progress_text="已恢复任务结果")
                if delivery.get("status") == "interrupted":
                    return _save(job, status="interrupted", error="执行已中断，重新开始时将尝试复用已保存规则")
            except (requests.RequestException, ValueError, TypeError):
                current_app.logger.warning("Clinical result recovery temporarily unavailable: %s", job.id)
        if execution.get("run_id") == job.run_id and execution.get("agent_task_id"):
            try:
                response = requests.get(
                    _agent_url() + "/api/tasks/" + execution["agent_task_id"] + "/status",
                    timeout=(2, 3),
                )
                if response.status_code == 404:
                    _save(job, status="interrupted", error="Agent 执行记录已丢失，已有材料仍保留")
                else:
                    response.raise_for_status()
                    remote = response.json()
                    if remote.get("status") == "running":
                        _save(job, heartbeat_at=_now(), progress_text="Agent 正在执行，等待下一阶段结果")
                    elif remote.get("status") in {"failed", "cancelled"}:
                        errors = [e.get("data", {}).get("error") for e in remote.get("events", []) if e.get("type") == "error"]
                        _save(job, status="failed", error=next((e for e in reversed(errors) if e), "Agent 未完成任务"))
                    elif remote.get("status") == "completed":
                        _save(job, status="interrupted", error="Agent 已结束，但结果交付未确认；请核对后再重新执行")
            except (requests.RequestException, ValueError, TypeError):
                current_app.logger.warning("Unable to reconcile clinical task %s", job.id)
    return job


def _save(job, **values):
    for key, value in values.items():
        setattr(job, key, value)
    job.updated_at = _now()
    db.session.commit()
    return job


def _reference_folder(job):
    root = Path(current_app.config["UPLOAD_FOLDER"]).resolve() / "clinical-creation" / job.id
    root.mkdir(parents=True, exist_ok=True)
    return root


def _worker_heartbeat(app, job_id, run_id, stop):
    with app.app_context():
        while not stop.wait(5):
            try:
                job = db.session.get(ClinicalCreationJob, job_id)
                if not job or job.status != "running" or job.run_id != run_id:
                    return
                _save(job, heartbeat_at=_now())
            except Exception:
                db.session.rollback()
                app.logger.exception("Clinical task heartbeat failed: job=%s run=%s", job_id, run_id)
            finally:
                db.session.remove()


def _generate_worker(app, job_id, run_id):
    stop = threading.Event()
    heartbeat = threading.Thread(target=_worker_heartbeat, args=(app, job_id, run_id, stop), daemon=True)
    heartbeat.start()
    try:
        with app.app_context():
            job = db.session.get(ClinicalCreationJob, job_id)
            if not job or job.run_id != run_id:
                return
            intake = json.loads(job.intake_json or "{}")
            draft = intake.get("formDraft") or {}
            narrative = job.description.strip()
            messages = json.loads(job.messages_json or "[]")
            user_turns = [str(item.get("text") or "").strip() for item in messages
                          if item.get("role") == "user" and str(item.get("text") or "").strip()]
            if user_turns:
                narrative += "\n对话中的补充与更正：\n" + "\n".join(user_turns[-10:])[:10000]
            if draft.get("free_narrative"):
                narrative += "\n助手整理的需求：" + str(draft["free_narrative"])[:5000]
            if job.notes.strip():
                narrative += "\n补充要求：" + job.notes.strip()
            data = {
                "model_name": job.name, "free_narrative": narrative,
                "domain": "clinical", "clinical_task": draft.get("scenario") or "",
                "generation_mode": "reproduce" if job.mode == "paper" else "new_design",
                "industry": "临床医疗", "scenario": draft.get("scenario") or "",
                "technology": "AI", "algorithm_category": draft.get("algorithm_category") or "",
                "category_params": json.dumps(draft.get("category_params") or {}, ensure_ascii=False),
                "reference_notes": job.notes,
                "resume_token": (intake.get("execution") or {}).get("resume_token", ""),
            }
            with ExitStack() as stack:
                files = None
                if job.mode == "paper":
                    reference = stack.enter_context(open(job.reference_path, "rb"))
                    files = {"file": (job.reference_name, reference, "application/octet-stream")}
                response = stack.enter_context(requests.post(
                    _agent_url() + "/api/agent/aml_auto_generate",
                    data=data, files=files, stream=True, timeout=(20, 1200),
                ))
                response.raise_for_status()
                agent_task_id = response.headers.get("X-Task-ID")
                if agent_task_id:
                    db.session.remove()
                    current = db.session.get(ClinicalCreationJob, job_id)
                    if not current or current.run_id != run_id:
                        return
                    metadata = json.loads(current.intake_json or "{}")
                    metadata["execution"] = {"run_id": run_id, "agent_task_id": agent_task_id,
                                             "resume_token": response.headers.get("X-Clinical-Run", "")}
                    _save(current, intake_json=json.dumps(metadata, ensure_ascii=False))
                result = None
                error = None
                for line in response.iter_lines():
                    if not line or not line.startswith(b"data:"):
                        continue
                    event = json.loads(line[5:].strip().decode("utf-8"))
                    stage_labels = {"reading": "正在读取论文", "rules": "正在核对评分规则",
                                    "implementation": "正在生成算法模型", "verification": "正在验证计算结果"}
                    if event.get("clinical_stage") in stage_labels:
                        db.session.remove()
                        current = db.session.get(ClinicalCreationJob, job_id)
                        if not current or current.run_id != run_id:
                            return
                        metadata = json.loads(current.intake_json or "{}")
                        metadata["clinical_stage"] = event["clinical_stage"]
                        _save(current, intake_json=json.dumps(metadata, ensure_ascii=False),
                              progress_text=stage_labels[event["clinical_stage"]], heartbeat_at=_now())
                    if event.get("step"):
                        step = min(int(event["step"]), 40)
                        db.session.remove()
                        current = db.session.get(ClinicalCreationJob, job_id)
                        if not current or current.run_id != run_id:
                            return
                        stage = json.loads(current.intake_json or "{}").get("clinical_stage")
                        _save(current, heartbeat_at=_now(), progress_step=step,
                              progress_text=stage_labels.get(stage, "正在分析资料并生成算法模型"))
                    if event.get("error"):
                        error = str(event["error"])
                    if event.get("is_final_result"):
                        result = (event.get("final_results") or {}).get("aml_generate_result")
                        error = event.get("error") or error
                db.session.remove()
                current = db.session.get(ClinicalCreationJob, job_id)
                if not current or current.run_id != run_id:
                    return
                if not error and isinstance(result, dict) and current.mode == "paper":
                    from app.services.clinical_reproduction import reproduction_gaps
                    gaps = reproduction_gaps(result)
                    if not gaps and result.get("reproduction", {}).get("status") == "pending_runtime":
                        try:
                            from app.services.clinical_reproduction import verify_candidate
                            verify_candidate(result, _reference_folder(current) / run_id)
                        except Exception as exc:
                            gaps = ["平台运行验证未通过：" + str(exc)[:500]]
                    if gaps:
                        encoded = json.dumps(result, ensure_ascii=False)
                        if len(encoded.encode("utf-8")) > MAX_RESULT_BYTES:
                            raise ValueError("生成结果超过 2 MB")
                        _save(current, status="needs_review", result_json=encoded,
                              error="；".join(gaps)[:1000], progress_text="请补充或核对论文规则")
                        return
                if error or not isinstance(result, dict) or not str(result.get("generated_code") or "").strip():
                    raise ValueError(error or "生成任务没有返回可用的算法源码")
                encoded = json.dumps(result, ensure_ascii=False)
                if len(encoded.encode("utf-8")) > MAX_RESULT_BYTES:
                    raise ValueError("生成结果超过 2 MB")
                _save(current, status="completed", result_json=encoded,
                      progress_text="生成完成，可保存并试用", error=None)
    except Exception as exc:
        app.logger.exception("Clinical creation generation failed: %s", job_id)
        with app.app_context():
            current = db.session.get(ClinicalCreationJob, job_id)
            if current and current.run_id == run_id:
                _save(current, status="failed", error=str(exc)[:1000], progress_text="生成失败")
    finally:
        stop.set()
        heartbeat.join(timeout=1)


@api.route("/catalog")
class Catalog(Resource):
    def get(self):
        return public_catalog()


@api.route("/jobs")
class Jobs(Resource):
    def get(self):
        user = _login()
        jobs = ClinicalCreationJob.query.filter_by(owner_id=str(user.id)).order_by(
            ClinicalCreationJob.updated_at.desc()).limit(30).all()
        return {"jobs": [_job(job.id, user).snapshot(include_result=False) for job in jobs]}

    def post(self):
        user = _login()
        body = request.get_json(silent=True) or {}
        mode = body.get("mode")
        if mode not in {"conversation", "paper"}:
            api.abort(400, "请选择对话创建或论文复现")
        dept_id = body.get("departmentId") or "general"
        if not department(dept_id):
            api.abort(400, "请选择有效科室")
        selected = None
        suggested = None
        if body.get("suggestedPaperId"):
            suggested = paper(body["suggestedPaperId"])
            if not suggested or mode != "paper" or dept_id not in suggested["departmentIds"]:
                api.abort(400, "请选择本科室的论文")
            if body.get("paperVersion") != suggested["version"]:
                api.abort(409, "论文版本已更新，请刷新后重试")
        if body.get("paperId"):
            selected = paper(body["paperId"])
            if not selected or mode != "paper":
                api.abort(400, "请选择有效的示例论文")
            if not has_materials(selected):
                api.abort(409, "示例论文文件暂不可用，请稍后重试")
            if dept_id not in selected["departmentIds"]:
                api.abort(400, "论文不属于所选科室")
            if body.get("paperVersion") != selected["version"]:
                api.abort(409, "论文版本已更新，请刷新后重试")
        job = ClinicalCreationJob(id=str(uuid.uuid4()), owner_id=str(user.id), mode=mode,
                                  description=str(body.get("description") or "")[:10000])
        metadata = {"departmentId": dept_id, "sourceType": "example" if selected else mode}
        if suggested and not selected:
            metadata["suggestedPaperId"] = suggested["id"]
            job.name = suggested["modelName"]
            job.description = "依据上传论文复现其中可完整实现的预测模型或评分计算。"
            job.notes = "希望复现“" + suggested["modelName"] + "”。请依据原文的公式、变量定义、单位及参数实现计算；缺少必要材料时明确说明，不自行补全。"
        if selected:
            metadata.update(paperId=selected["id"], paperVersion=selected["version"], paperSha256=selected["sha256"])
            try:
                attach_paper(job, selected)
            except (OSError, ValueError):
                api.abort(409, "示例材料暂不可用，请联系维护人员")
        job.intake_json = json.dumps({"catalog": metadata}, ensure_ascii=False)
        db.session.add(job)
        db.session.commit()
        return {"job": job.snapshot()}, 201


@api.route("/jobs/<string:job_id>")
class Job(Resource):
    def get(self, job_id):
        return {"job": _job(job_id, _login()).snapshot()}

    def patch(self, job_id):
        job = _job(job_id, _login())
        if job.status in {"running", "published"}:
            api.abort(409, "当前状态不能修改创建信息")
        body = request.get_json(silent=True) or {}
        values = {}
        if "departmentId" in body:
            if not department(body["departmentId"]):
                api.abort(400, "请选择有效科室")
            intake = json.loads(job.intake_json or "{}")
            meta = intake.setdefault("catalog", {})
            if meta.get("departmentId") != body["departmentId"]:
                meta["departmentId"] = body["departmentId"]
                values["intake_json"] = json.dumps(intake, ensure_ascii=False)
        for field, limit in (("name", 100), ("description", 10000), ("notes", 5000)):
            if field in body:
                value = str(body[field] or "")[:limit]
                if value != getattr(job, field):
                    values[field] = value
        if "referenceReviewed" in body:
            value = bool(body["referenceReviewed"])
            if value != job.reference_reviewed:
                values["reference_reviewed"] = value
        if any(key != "intake_json" for key in values) and job.status in {"completed", "failed", "interrupted", "needs_review"}:
            values.update(status="draft", result_json=None, error=None, progress_step=0)
        return {"job": (_save(job, **values) if values else job).snapshot()}


@api.route("/jobs/<string:job_id>/reference")
class Reference(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.mode != "paper" or job.status in {"running", "published"}:
            api.abort(409, "当前任务不能上传论文")
        upload = request.files.get("file")
        if not upload or not upload.filename:
            api.abort(400, "请选择 PDF 或 DOCX 论文")
        suffix = Path(upload.filename).suffix.lower()
        if suffix not in {".pdf", ".docx"}:
            api.abort(400, "论文仅支持 PDF 或 DOCX")
        raw = upload.read(MAX_REFERENCE_BYTES + 1)
        if not raw:
            api.abort(400, "论文文件为空")
        if len(raw) > MAX_REFERENCE_BYTES:
            api.abort(400, "论文不能超过 10 MB")
        path = _reference_folder(job) / ("main" + suffix)
        path.write_bytes(raw)
        # Upload only persists the source. The generation pipeline reads it once,
        # including OCR when needed; a preview or human review is not a prerequisite.
        preview = ""
        if job.reference_path and job.reference_path != str(path):
            Path(job.reference_path).unlink(missing_ok=True)
        intake = json.loads(job.intake_json or "{}")
        previous_catalog = intake.get("catalog") or {}
        replaced_example = bool(previous_catalog.get("paperId"))
        first_upload = not job.reference_path
        # A new source must never inherit a curated paper's rules or resume token.
        intake = {"catalog": {"departmentId": previous_catalog.get("departmentId", "general"), "sourceType": "paper"}}
        _save(job, name=Path(upload.filename).stem[:100] if replaced_example else job.name or Path(upload.filename).stem[:100],
              description="依据上传论文复现其中可完整实现的公式或评分计算；缺少参数时明确报告，不自行补全。" if replaced_example else job.description or "依据上传论文复现其中可完整实现的公式或评分计算；缺少参数时明确报告，不自行补全。",
              notes=job.notes if first_upload else "", intake_json=json.dumps(intake, ensure_ascii=False),
              reference_name=upload.filename[:255], reference_path=str(path),
              reference_preview=preview, reference_reviewed=False,
              status="draft", result_json=None, error=None, progress_step=0, progress_text="")
        return {"job": job.snapshot()}

    def get(self, job_id):
        job = _job(job_id, _login())
        if not job.reference_path or not Path(job.reference_path).is_file():
            api.abort(404, "论文文件不存在")
        return send_file(job.reference_path, as_attachment=True, download_name=job.reference_name)


@api.route("/jobs/<string:job_id>/intake")
class Intake(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.mode != "conversation" or job.status in {"running", "published"}:
            api.abort(409, "当前任务不能继续对话")
        body = request.get_json(silent=True) or {}
        message = str(body.get("message") or "").strip()[:4000]
        if not message:
            api.abort(400, "请输入模型需求")
        messages = json.loads(job.messages_json or "[]")
        intake = json.loads(job.intake_json or "{}")
        try:
            response = requests.post(_agent_url() + "/api/agent/aml_scenario_intake", data={
                "message": message, "domain": "clinical",
                "session_id": intake.get("session_id") or "",
                "partial_form": json.dumps(intake.get("formDraft") or {}, ensure_ascii=False),
                "followup_count": str(sum(1 for item in messages if item.get("role") == "assistant")),
            }, timeout=(15, 120))
            response.raise_for_status()
            reply = response.json()
        except (requests.RequestException, ValueError) as exc:
            return {"message": f"需求整理暂时不可用：{exc}"}, 502
        messages.append({"role": "user", "text": message})
        answer = str(reply.get("text") or reply.get("hint") or "请继续补充模型需求")[:3000]
        messages.append({"role": "assistant", "text": answer})
        draft = reply.get("formDraft") if isinstance(reply.get("formDraft"), dict) else {}
        name = job.name or str(draft.get("model_name") or "")[:100]
        description = job.description or message
        reply["catalog"] = intake.get("catalog", {})
        _save(job, name=name, description=description,
              messages_json=json.dumps(messages[-40:], ensure_ascii=False),
              intake_json=json.dumps(reply, ensure_ascii=False), status="draft",
              result_json=None, error=None)
        return {"job": job.snapshot()}


@api.route("/jobs/<string:job_id>/generate")
class Generate(Resource):
    def post(self, job_id):
        job = _job(job_id, _login())
        if job.status == "running":
            return {"job": job.snapshot()}
        if job.status == "published":
            api.abort(409, "模型已经保存")
        if not job.name.strip() or not job.description.strip():
            api.abort(400, "请填写模型名称和需求描述")
        if job.mode == "paper" and (not job.reference_path or
                                    not Path(job.reference_path).is_file()):
            api.abort(400, "请先上传论文")
        run_id = str(uuid.uuid4())
        updated = ClinicalCreationJob.query.filter(
            ClinicalCreationJob.id == job_id,
            ClinicalCreationJob.status.in_(["draft", "failed", "interrupted", "completed", "needs_review"]),
        ).update({"status": "running", "run_id": run_id, "heartbeat_at": _now(),
                  "progress_step": 0, "progress_text": "等待 Agent 接收任务",
                  "result_json": None, "error": None, "updated_at": _now()}, synchronize_session=False)
        db.session.commit()
        if updated != 1:
            api.abort(409, "任务状态已改变，请刷新")
        app = current_app._get_current_object()
        threading.Thread(target=_generate_worker, args=(app, job_id, run_id), daemon=True).start()
        return {"job": _job(job_id, _login()).snapshot()}, 202


@api.route("/jobs/<string:job_id>/publish")
class Publish(Resource):
    def post(self, job_id):
        user = _login()
        job = _job(job_id, user)
        if job.service_id:
            return {"job": job.snapshot()}
        if job.status != "completed" or not job.result_json:
            api.abort(409, "请先完成算法生成")
        result = json.loads(job.result_json)
        code = str(result.get("generated_code") or "")
        if not code.strip():
            api.abort(400, "生成结果缺少源码")
        filename = secure_filename(result.get("code_filename") or "generated_algorithm.py")
        if not filename.lower().endswith(".py"):
            filename = "generated_algorithm.py"
        with ExitStack() as stack:
            source = FileStorage(stream=io.BytesIO(code.encode("utf-8")), filename=filename)
            references = []
            if job.mode == "paper" and job.reference_path:
                handle = stack.enter_context(open(job.reference_path, "rb"))
                reference_name = (secure_filename(Path(job.reference_name).stem) or "paper") + Path(job.reference_name).suffix.lower()
                references.append(FileStorage(stream=handle, filename=reference_name))
            spec = result.get("algorithm_spec") if isinstance(result.get("algorithm_spec"), dict) else {}
            inputs = spec.get("inputs") if isinstance(spec.get("inputs"), list) else []
            inputs = [item for item in inputs if isinstance(item, dict)]
            output = spec.get("output") if isinstance(spec.get("output"), dict) else {}
            summary = result.get("model_summary") if isinstance(result.get("model_summary"), dict) else {}
            card = {
                "task": "", "specialty": "", "population": "", "timepoint": "",
                "exclusions": "", "inputs": ", ".join(str(item.get("label") or item.get("name")) for item in inputs or []),
                "units": "", "missing": "", "output": str(output.get("description") or ""),
                "horizon": "", "threshold": "", "dataSource": "未提供独立验证数据",
                "sampleSize": "未开展独立验证", "validation": "平台合成样例运行",
                "results": "尚无真实数据评估结果", "version": "0.1.0",
                "team": "", "references": job.reference_name if job.mode == "paper" else "",
                "limitations": str(summary.get("limitations") or "尚未完成独立临床验证"),
                "intendedUse": "研究与实现核对，不用于独立诊疗决策", "reviewStatus": "pending",
            }
            catalog_meta = json.loads(job.intake_json or "{}").get("catalog") or {}
            dept = department(catalog_meta.get("departmentId"))
            if dept:
                card.update(specialty=dept["name"], departmentIds=[dept["id"]])
            card["paperId"] = catalog_meta.get("paperId")
            card["paperVersion"] = catalog_meta.get("paperVersion")
            meta = {
                "name": job.name, "domain": "health", "industry": "临床医疗",
                "scenario": "", "technology": "AI", "attribute": "custom",
                "creator_id": user.id, "reference_files": references,
                "source": {"popoverTitle": job.name, "companyName": "众智工场供应商",
                           "msIntroduce": job.description,
                           "companyIntroduce": "ZZF_CLINICAL_V1:" + json.dumps(card, ensure_ascii=False),
                           "reproductionMode": job.mode == "paper",
                           "generationEvidence": ["依据论文复现" if job.mode == "paper" else "对话创建",
                                                  job.reference_name or "未提供论文"]},
            }
            if isinstance(inputs, list) and inputs and result.get("smoke_input"):
                meta["algorithm_spec"] = spec
                meta["smoke_input"] = result["smoke_input"]
            try:
                service = service_service.upload_scenario_generated_algorithm(source, meta)
            except ServiceServiceError as exc:
                return {"message": str(exc)}, 400
        _save(job, status="published", service_id=service["id"])
        return {"job": job.snapshot(), "service": service}
