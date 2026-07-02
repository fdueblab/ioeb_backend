"""全量 mock 数据灌库（manage.py seed_db 使用）。"""

import json
import uuid
from pathlib import Path

from app.extensions import db
from app.models import (
    Dictionary,
    Role,
    RolePermission,
    Service,
    ServiceApi,
    ServiceApiParameter,
    ServiceApiTool,
    ServiceNorm,
    ServiceSource,
    User,
)
from mocks.dictionary import MOCK_DICTIONARIES
from mocks.service import (
    MOCK_SERVICE_API_PARAMETERS,
    MOCK_SERVICE_API_TOOLS,
    MOCK_SERVICE_APIS,
    MOCK_SERVICE_NORMS,
    MOCK_SERVICE_SOURCES,
    MOCK_SERVICES,
)
from mocks.user import MOCK_ROLES, MOCK_ROLES_PERMISSIONS, MOCK_USERS

_MCP_CATALOG = (
    Path(__file__).resolve().parents[2] / "external-mcp" / "service_catalog.json"
)
_MCP_SERVICE_DEFAULTS = {
    "attribute": "open_source",
    "industry": "0",
    "scenario": "0",
    "technology": "0",
    "network": "ioeb_app-network",
    "volume": "",
    "status": "released",
    "number": 0,
    "deleted": 0,
    "creator_id": "",
}


def seed_all_mock_data():
    for user in MOCK_USERS:
        db.session.add(User(**user))
    for role in MOCK_ROLES:
        db.session.add(Role(**role))
    for role_permission in MOCK_ROLES_PERMISSIONS:
        db.session.add(RolePermission(**role_permission))
    for service in MOCK_SERVICES:
        db.session.add(Service(**service))
    for norm in MOCK_SERVICE_NORMS:
        db.session.add(ServiceNorm(**norm))
    for source in MOCK_SERVICE_SOURCES:
        db.session.add(ServiceSource(**source))
    for api in MOCK_SERVICE_APIS:
        db.session.add(ServiceApi(**api))
    for param in MOCK_SERVICE_API_PARAMETERS:
        db.session.add(ServiceApiParameter(**param))
    for tool in MOCK_SERVICE_API_TOOLS:
        db.session.add(ServiceApiTool(**tool))
    for dictionary in MOCK_DICTIONARIES:
        db.session.add(Dictionary(**dictionary))
    db.session.commit()


def seed_mcp_catalog():
    """把 external-mcp/service_catalog.json 医疗 MCP 入库（已存在则同步 url）。"""
    if not _MCP_CATALOG.is_file():
        return 0
    catalog = json.loads(_MCP_CATALOG.read_text(encoding="utf-8"))
    inserted = 0
    for svc in catalog.get("services", []):
        sid = svc["serviceId"]
        catalog_url = svc["url"]
        existing = Service.query.get(sid)
        if existing:
            api = ServiceApi.query.filter_by(service_id=sid).first()
            if api and api.url != catalog_url:
                api.url = catalog_url
                api.method = svc.get("mcpMethod", "sse")
            continue
        db.session.add(
            Service(
                id=sid,
                name=svc["name"],
                attribute=_MCP_SERVICE_DEFAULTS["attribute"],
                type=catalog.get("type", "atomic_mcp"),
                domain=catalog.get("domain", "health"),
                industry=_MCP_SERVICE_DEFAULTS["industry"],
                scenario=_MCP_SERVICE_DEFAULTS["scenario"],
                technology=_MCP_SERVICE_DEFAULTS["technology"],
                network=_MCP_SERVICE_DEFAULTS["network"],
                port=f"{svc['port']}/tcp",
                volume=_MCP_SERVICE_DEFAULTS["volume"],
                status=_MCP_SERVICE_DEFAULTS["status"],
                number=_MCP_SERVICE_DEFAULTS["number"],
                deleted=_MCP_SERVICE_DEFAULTS["deleted"],
                creator_id=_MCP_SERVICE_DEFAULTS["creator_id"],
            )
        )
        api_id = str(uuid.uuid4())
        db.session.add(
            ServiceApi(
                id=api_id,
                service_id=sid,
                name=svc["name"],
                url=svc["url"],
                method=svc.get("mcpMethod", "sse"),
                des=svc["des"],
                parameter_type=0,
                response_type=0,
                is_fake=False,
            )
        )
        for tool in svc.get("tools", []):
            db.session.add(
                ServiceApiTool(
                    id=str(uuid.uuid4()),
                    api_id=api_id,
                    name=tool["name"],
                    description=tool.get("description", ""),
                )
            )
        inserted += 1
    db.session.commit()
    return inserted
