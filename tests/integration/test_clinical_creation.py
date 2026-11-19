"""The simplified creation flow survives a new request and keeps jobs private."""

import datetime
import io
import json

import pytest

from app import create_app
from app.extensions import db
from app.models import Role, User, UserToken
from app.models.clinical_creation_job import ClinicalCreationJob


@pytest.fixture
def creation_client(tmp_path):
    app = create_app("testing")
    app.config["UPLOAD_FOLDER"] = str(tmp_path)
    now = int(datetime.datetime.now().timestamp() * 1000)
    with app.test_client() as client, app.app_context():
        db.session.add(Role(id="user", name="用户", describe="普通用户", status=1, deleted=0, create_time=now))
        for user_id in ("author", "other"):
            db.session.add(User(id=user_id, username=user_id, name=user_id, password="x",
                                role_id="user", status=1, deleted=0, create_time=now))
            db.session.add(UserToken(user_id=user_id, token=f"{user_id}-token", expires_at=now + 86400000))
        db.session.commit()
        yield client, app
        db.session.remove()
        db.drop_all()


def auth(user_id="author"):
    return {"Access-Token": f"{user_id}-token"}


def test_catalog_covers_departments_and_example_is_private(creation_client, monkeypatch):
    from app.api.namespaces import clinical_creation_ns as routes
    def unexpected_fetch(*args, **kwargs):
        pytest.fail('Selecting a stored paper must not require an external download or Agent call')
    monkeypatch.setattr(routes.requests, 'get', unexpected_fetch)
    monkeypatch.setattr(routes.requests, 'post', unexpected_fetch)
    client, _ = creation_client
    catalog = client.get('/api/clinical-creation/catalog').get_json()
    assert len(catalog['departments']) == 13
    for dept in catalog['departments']:
        assert any(dept['id'] in p['departmentIds'] for p in catalog['papers'])
    ready = [p for p in catalog['papers'] if p['canCreate']]
    assert len(catalog['papers']) == 11
    assert {p['id'] for p in ready} == {p['id'] for p in catalog['papers']} - {'adnex'}
    unavailable = next(p for p in catalog['papers'] if p['id'] == 'adnex')
    assert client.post('/api/clinical-creation/jobs', headers=auth(), json=dict(mode='paper', departmentId='oncology', paperId='adnex', paperVersion=unavailable['version'])).status_code == 409
    for paper in ready:
        payload = dict(mode='paper', departmentId=paper['departmentIds'][0], paperId=paper['id'], paperVersion=paper['version'])
        assert client.post('/api/clinical-creation/jobs', json=payload).status_code == 401
        created = client.post('/api/clinical-creation/jobs', headers=auth(), json=payload)
        assert created.status_code == 201
        job = created.get_json()['job']
        assert job['departmentId'] == payload['departmentId']
        assert job['referencePreview'] and job['notes'] and not job['referenceReviewed']
        path = '/api/clinical-creation/jobs/' + job['id'] + '/reference'
        assert client.get(path, headers=auth('other')).status_code == 404
        import hashlib
        assert hashlib.sha256(client.get(path, headers=auth()).data).hexdigest() == paper['sha256']
        assert client.post('/api/clinical-creation/jobs', headers=auth(), json={**payload, 'paperVersion':'stale'}).status_code == 409
        wrong_dept = next(d['id'] for d in catalog['departments'] if d['id'] not in paper['departmentIds'])
        assert client.post('/api/clinical-creation/jobs', headers=auth(), json={**payload, 'departmentId':wrong_dept}).status_code == 400
    assert client.post('/api/clinical-creation/jobs', headers=auth(), json=dict(mode='paper', departmentId='cardiology', paperId='unknown', paperVersion='1')).status_code == 400


@pytest.mark.parametrize('failure', ['missing', 'corrupt'])
def test_unavailable_example_does_not_create_empty_job(creation_client, monkeypatch, tmp_path, failure):
    from app.services import clinical_catalog
    client, _ = creation_client
    original = clinical_catalog.ROOT
    (tmp_path / 'catalog.json').write_bytes((original / 'catalog.json').read_bytes())
    folder = tmp_path / 'qrisk3'
    folder.mkdir()
    (folder / 'notes.txt').write_text('preset', encoding='utf-8')
    if failure == 'corrupt':
        (folder / 'paper.pdf').write_bytes(b'%PDF-modified')
    monkeypatch.setattr(clinical_catalog, 'ROOT', tmp_path)
    version = clinical_catalog.paper('qrisk3')['version']
    response = client.post('/api/clinical-creation/jobs', headers=auth(), json=dict(mode='paper', departmentId='cardiology', paperId='qrisk3', paperVersion=version))
    assert response.status_code == 409
    assert client.get('/api/clinical-creation/jobs', headers=auth()).get_json()['jobs'] == []


def test_replacing_example_clears_old_rules_and_provenance(creation_client, monkeypatch):
    from app.api.namespaces import clinical_creation_ns as routes
    client, _ = creation_client
    created = client.post('/api/clinical-creation/jobs', headers=auth(), json=dict(mode='paper', departmentId='emergency', paperId='priest', paperVersion='1'))
    job_id = created.get_json()['job']['id']
    class Reply:
        def raise_for_status(self): pass
        def json(self): return {'text':'new source'}
    monkeypatch.setattr(routes.requests, 'post', lambda *a, **kw: Reply())
    response = client.post(f'/api/clinical-creation/jobs/{job_id}/reference', headers=auth(), data={'file':(io.BytesIO(b'new paper'), 'replacement.pdf')})
    job = response.get_json()['job']
    assert job['departmentId'] == 'emergency'
    assert job['name'] == 'replacement' and job['notes'] == ''
    assert job['intake']['catalog'] == {'departmentId':'emergency', 'sourceType':'paper'}


def test_publish_keeps_selected_department_and_paper_version(creation_client, monkeypatch):
    from app.api.namespaces import clinical_creation_ns as routes
    client, _ = creation_client
    created = client.post('/api/clinical-creation/jobs', headers=auth(), json=dict(mode='paper', departmentId='respiratory', paperId='abc2sph', paperVersion='1'))
    job_id = created.get_json()['job']['id']
    job = db.session.get(ClinicalCreationJob, job_id)
    job.status = 'completed'
    job.result_json = json.dumps({'generated_code':'def main_process(): return 0'})
    db.session.commit()
    captured = []
    def upload(source, meta):
        captured.append(meta)
        return {'id':'synthetic-service'}
    monkeypatch.setattr(routes.service_service, 'upload_scenario_generated_algorithm', upload)
    response = client.post(f'/api/clinical-creation/jobs/{job_id}/publish', headers=auth())
    assert response.status_code == 200
    card = json.loads(captured[0]['source']['companyIntroduce'].split(':',1)[1])
    assert card['departmentIds'] == ['respiratory']
    assert card['specialty'] == '呼吸内科'
    assert (card['paperId'],card['paperVersion']) == ('abc2sph','1')


@pytest.mark.parametrize('source', ['upload', 'priest', 'abc2sph', 'qrisk3', 'suggested'])
def test_paper_can_generate_without_review_or_preview(creation_client, monkeypatch, source):
    from app.api.namespaces import clinical_creation_ns as routes
    client, _ = creation_client
    payload = {'mode':'paper', 'departmentId':'respiratory'}
    from app.services.clinical_catalog import paper
    if source in {'priest', 'abc2sph', 'qrisk3'}:
        selected = paper(source)
        payload.update(departmentId=selected['departmentIds'][0], paperId=source, paperVersion=selected['version'])
    if source == 'suggested':
        payload.update(departmentId='cardiology', suggestedPaperId='qrisk3', paperVersion=paper('qrisk3')['version'])
    job = client.post('/api/clinical-creation/jobs', headers=auth(), json=payload).get_json()['job']
    path = '/api/clinical-creation/jobs/' + job['id']
    launches = []
    class Worker:
        def __init__(self, **kwargs): self.kwargs = kwargs
        def start(self): launches.append(self.kwargs)
    monkeypatch.setattr(routes.threading, 'Thread', Worker)
    if source in {'upload', 'suggested'}:
        assert client.post(path + '/generate', headers=auth()).status_code == 400
        if source == 'suggested': assert 'QRISK3' in job['notes']
        else:
            client.patch(path, headers=auth(), json={'notes':'只复现评分公式'})
        job = client.post(path + '/reference', headers=auth(), data={'file':(io.BytesIO(b'%PDF-fixture'), 'source.pdf')}).get_json()['job']
        assert job['notes'] and job['referencePreview'] == ''
    assert not job['referenceReviewed']
    # Optional prompts can be edited or cleared; neither requires review.
    client.patch(path, headers=auth(), json={'notes':''})
    response = client.post(path + '/generate', headers=auth())
    assert response.status_code == 202, response.get_json()
    assert response.get_json()['job']['status'] == 'running'
    assert len(launches) == 1
    assert client.post(path + '/generate', headers=auth()).status_code == 200
    assert len(launches) == 1


@pytest.mark.parametrize("remote_status,expected", [("running", "running"), ("failed", "failed")])
def test_stale_heartbeat_checks_agent(creation_client, monkeypatch, remote_status, expected):
    client, _ = creation_client
    from app.api.namespaces import clinical_creation_ns as routes
    created = client.post("/api/clinical-creation/jobs", headers=auth(), json={"mode": "conversation"})
    job_id = created.get_json()["job"]["id"]
    job = db.session.get(ClinicalCreationJob, job_id)
    job.status = "running"
    job.run_id = "attempt"
    job.heartbeat_at = 1
    job.intake_json = json.dumps({"execution": {"run_id": "attempt", "agent_task_id": "remote"}})
    db.session.commit()

    class Reply:
        status_code = 200
        def raise_for_status(self):
            pass
        def json(self):
            return {"status": remote_status, "events": []}

    monkeypatch.setattr(routes.requests, "get", lambda *a, **kw: Reply())
    result = client.get(f"/api/clinical-creation/jobs/{job_id}", headers=auth()).get_json()["job"]
    assert result["status"] == expected


def test_unknown_stale_task_is_not_declared_dead(creation_client):
    client, _ = creation_client
    created = client.post("/api/clinical-creation/jobs", headers=auth(), json={"mode": "conversation"})
    job_id = created.get_json()["job"]["id"]
    job = db.session.get(ClinicalCreationJob, job_id)
    job.status = "running"
    job.heartbeat_at = 1
    db.session.commit()
    result = client.get(f"/api/clinical-creation/jobs/{job_id}", headers=auth()).get_json()["job"]
    assert result["status"] == "running"
    assert "确认" in result["progressText"]


def test_job_is_restored_only_for_its_owner_and_unchanged_save_keeps_result(creation_client):
    client, _ = creation_client
    created = client.post("/api/clinical-creation/jobs", headers=auth(), json={"mode": "conversation"})
    assert created.status_code == 201, created.get_json()
    job_id = created.get_json()["job"]["id"]
    path = f"/api/clinical-creation/jobs/{job_id}"

    assert client.get(path, headers=auth("other")).status_code == 404
    assert client.patch(path, headers=auth("other"), json={"name": "stolen"}).status_code == 404
    saved = client.patch(path, headers=auth(), json={"name": "BMI", "description": "计算 BMI"})
    assert saved.status_code == 200, saved.get_json()
    restored = client.get(path, headers=auth()).get_json()["job"]
    assert (restored["name"], restored["description"]) == ("BMI", "计算 BMI")
    assert any(item["id"] == job_id for item in client.get("/api/clinical-creation/jobs", headers=auth()).get_json()["jobs"])

    job = db.session.get(ClinicalCreationJob, job_id)
    job.status = "completed"
    job.result_json = json.dumps({"generated_code": "def bmi(): pass"})
    db.session.commit()
    unchanged = client.patch(path, headers=auth(), json={"name": "BMI", "description": "计算 BMI"})
    assert unchanged.get_json()["job"]["status"] == "completed"
    assert unchanged.get_json()["job"]["result"]["generated_code"] == "def bmi(): pass"
    moved = client.patch(path, headers=auth(), json={"departmentId": "endocrinology"}).get_json()["job"]
    assert moved["departmentId"] == "endocrinology"
    assert moved["status"] == "completed"
    assert moved["result"]["generated_code"] == "def bmi(): pass"


def test_paper_upload_is_private_and_does_not_wait_for_agent_preview(creation_client, monkeypatch):
    import app.api.namespaces.clinical_creation_ns as creation_ns

    client, _ = creation_client

    class PreviewResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"text": "研究使用年龄及体重计算评分。"}

    def unexpected_preview(*args, **kwargs):
        pytest.fail("Uploading must not depend on the Agent preview service")
    monkeypatch.setattr(creation_ns.requests, "post", unexpected_preview)
    job_id = client.post("/api/clinical-creation/jobs", headers=auth(), json={"mode": "paper"}).get_json()["job"]["id"]
    path = f"/api/clinical-creation/jobs/{job_id}/reference"
    uploaded = client.post(path, headers=auth(), data={"file": (io.BytesIO(b"paper"), "论文.pdf")},
                           content_type="multipart/form-data")
    assert uploaded.status_code == 200, uploaded.get_json()
    assert uploaded.get_json()["job"]["referencePreview"] == ""
    assert client.get(path, headers=auth("other")).status_code == 404
    assert client.get(path, headers=auth()).data == b"paper"
    assert client.get(f"/api/clinical-creation/jobs/{job_id}", headers=auth()).get_json()["job"]["referenceName"] == "论文.pdf"


@pytest.mark.parametrize("missing,remote_error,runtime_error,expected", [(False,False,False,"completed"),(True,False,False,"needs_review"),(False,True,False,"failed"),(False,False,True,"needs_review")])
def test_generation_delivery_and_private_resume_token(creation_client, monkeypatch, tmp_path, missing, remote_error, runtime_error, expected):
    client, app = creation_client
    from app.api.namespaces import clinical_creation_ns as routes
    job_id = client.post("/api/clinical-creation/jobs", headers=auth(), json={"mode":"paper"}).get_json()["job"]["id"]
    source = tmp_path / "paper.pdf"
    source.write_bytes(b"fixture")
    job = db.session.get(ClinicalCreationJob, job_id)
    job.reference_path = str(source)
    job.reference_name = "paper.pdf"
    job.status = "running"
    job.run_id = "attempt"
    db.session.commit()
    result = {"generated_code":"def main_process(age): return age", "reproduction":{"evidence":{
        "method_type":"score", "population":"adults", "outcome":"score", "horizon":"current",
        "rules":[] if missing else [{"input":"age","rule":"age","source":{"page":1,"location":"table","quote":"age"}}]}}}
    class Response:
        headers = {"X-Task-ID":"task", "X-Clinical-Run":"private-capability"}
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def raise_for_status(self): pass
        def iter_lines(self):
            if remote_error: yield b'data: {"error":"connection lost"}'
            yield ("data: " + json.dumps({"is_final_result":True,"final_results":{"aml_generate_result":result}})).encode()
    monkeypatch.setattr(routes.requests,"post",lambda *a,**kw: Response())
    from app.services import clinical_reproduction
    result["reproduction"]["status"] = "pending_runtime"
    verified = []
    def verify(candidate, folder):
        verified.append(candidate)
        if runtime_error:
            raise ValueError("fixture runtime failure")
        candidate["reproduction"]["status"] = "runtime_checked"
    monkeypatch.setattr(clinical_reproduction, "verify_candidate", verify)
    routes._generate_worker(app,job_id,"attempt")
    assert len(verified) == (0 if missing or remote_error else 1)
    db.session.remove()
    stored = db.session.get(ClinicalCreationJob,job_id)
    assert stored.status == expected
    assert json.loads(stored.intake_json)["execution"]["resume_token"] == "private-capability"
    visible = client.get(f"/api/clinical-creation/jobs/{job_id}",headers=auth()).get_json()
    assert "private-capability" not in json.dumps(visible)
