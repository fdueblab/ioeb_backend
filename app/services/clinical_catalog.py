"""Versioned clinical departments and curated paper material bundles."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'resources' / 'clinical_catalog'


def catalog():
    return json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))


def department(identifier):
    return next((d for d in catalog()['departments'] if d['id'] == identifier), None)


def paper(identifier):
    return next((p for p in catalog()['papers'] if p['id'] == identifier), None)


def bundle_path(item, filename):
    path = (ROOT / item['id'] / filename).resolve()
    path.relative_to(ROOT.resolve())
    return path


def public_catalog():
    data = catalog()
    for item in data['papers']:
        # Having a local source is independent of algorithm/clinical validation.
        item['canCreate'] = has_materials(item)
    return data


def has_materials(item):
    return bool(item.get('sha256')) and all(
        bundle_path(item, name).is_file() for name in ('paper.pdf', 'notes.txt'))


def attach_paper(job, item):
    """Copy a curated local source, never fetch an arbitrary client URL."""
    from app.api.namespaces.clinical_creation_ns import _reference_folder
    raw = bundle_path(item, 'paper.pdf').read_bytes()
    if not raw.startswith(b'%PDF-') or hashlib.sha256(raw).hexdigest() != item['sha256']:
        raise ValueError('示例论文版本不一致，请联系维护人员')
    target = _reference_folder(job) / 'main.pdf'
    target.write_bytes(raw)
    job.reference_path = str(target)
    job.reference_name = item['id'] + '.pdf'
    preview = bundle_path(item, 'preview.txt')
    job.reference_preview = preview.read_text(encoding='utf-8')[:12000] if preview.is_file() else ''
    job.notes = bundle_path(item, 'notes.txt').read_text(encoding='utf-8')
    job.name = item['modelName']
    job.description = item['scope']
    job.reference_reviewed = False
