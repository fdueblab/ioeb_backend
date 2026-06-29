"""Canonical published meta-app configuration helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Iterable


ARTIFACT_SCHEMA = "meta_app_artifact.v1"


def stable_hash(value: dict) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def default_runtime_spec(service_id: str = "{serviceId}") -> dict:
    return {
        "mode": "shared_agent",
        "docker": {
            "image": "fdueblab/meta-app-agent:latest",
            "containerName": f"meta-app-{service_id}",
            "restartPolicy": "unless-stopped",
        },
        "network": "ioeb_app-network",
        "ports": [{
            "protocol": "tcp",
            "containerPort": 1021,
            "hostIp": "0.0.0.0",
            "hostPort": 10021,
        }],
        "volumes": [{
            "source": "/var/opt/gitlab/mnt/user",
            "target": "/appdata/aml/metaApp",
            "mode": "rw",
        }],
    }


def build_agent_only_artifact(service, api, dependencies: Iterable) -> dict:
    bindings = []
    for dependency in dependencies:
        dependency_api = dependency.apis[0]
        is_fake = dependency_api.is_fake is True
        bindings.append({
            "serviceId": dependency.id,
            "serviceName": dependency.name,
            "isFake": is_fake,
            "source": "demo_fake_mcp" if is_fake else "real_mcp",
            "transport": str(dependency_api.method or "sse").lower(),
            "endpoint": dependency_api.url or "",
            "schemaHash": stable_hash({
                "tools": [tool.to_dict() for tool in dependency_api.tools]
            })[:16],
            "tools": [{
                "toolName": tool.name,
                "description": tool.description or "",
                "inputSchema": {},
            } for tool in dependency_api.tools],
        })
    body = {
        "schemaVersion": ARTIFACT_SCHEMA,
        "app": {
            "name": service.name,
            "domain": service.domain,
            "description": api.des or "",
        },
        "taskContract": {
            "goal": api.des or service.name,
            "domain": service.domain,
            "inputSlots": [{
                "name": api.input_name or "input",
                "type": "string",
                "required": True,
            }],
            "outputSlots": [{
                "name": api.output_name or "result",
                "type": "object",
                "required": True,
            }],
            "constraints": [],
            "successCriteria": [],
        },
        "runtime": {
            "mode": "agent_only",
            "serviceBindings": bindings,
            "fallbackPolicy": {
                "onApplicabilityMismatch": "run_slow_mode",
                "onBindingFailure": "run_slow_mode",
                "onToolFailure": "run_slow_mode",
                "onAssertionFailure": "run_slow_mode",
            },
            "agent": {
                "style": "react_slow_mode",
                "goldenPathDecision": "agent_internal",
            },
        },
        "goldenPaths": [],
    }
    return {"schemaVersion": ARTIFACT_SCHEMA, "artifactId": f"app-{stable_hash(body)[:16]}", **body}


def migrate_meta_app_services() -> int:
    """Backfill service_apis columns and rebuild deterministic artifacts for meta apps."""
    from sqlalchemy import inspect, text

    from app.extensions import db
    from app.models import Service

    column_types = {
        "simulation_build_id": "VARCHAR(64)",
        "meta_app_artifact_id": "VARCHAR(64)",
        "meta_app_artifact_hash": "VARCHAR(128)",
        "meta_app_artifact": "JSON",
        "run_mode": "VARCHAR(32)",
        "runtime_spec": "JSON",
    }
    existing = {row["name"] for row in inspect(db.engine).get_columns("service_apis")}
    with db.engine.begin() as connection:
        for name, sql_type in column_types.items():
            if name not in existing:
                connection.execute(text(f"ALTER TABLE service_apis ADD COLUMN {name} {sql_type}"))

    planned = []
    for service in Service.query.filter_by(type="meta", deleted=0).all():
        if len(service.apis) != 1:
            raise ValueError(f"元应用 {service.id} 必须且仅能有一个API")
        api = service.apis[0]
        dependency_ids = [value.strip() for value in (api.services or "").split(",") if value.strip()]
        dependencies = []
        for dependency_id in dependency_ids:
            dependency = Service.query.filter_by(id=dependency_id, deleted=0).first()
            if not dependency or len(dependency.apis) != 1:
                raise ValueError(f"元应用 {service.id} 依赖服务不可用: {dependency_id}")
            dependencies.append(dependency)
        planned.append((service, api, dependencies))

    try:
        for service, api, dependencies in planned:
            artifact = build_agent_only_artifact(service, api, dependencies)
            api.simulation_build_id = f"migration-{service.id}"
            api.meta_app_artifact_id = artifact["artifactId"]
            api.meta_app_artifact_hash = stable_hash(artifact)
            api.meta_app_artifact = artifact
            api.run_mode = "agent"
            api.runtime_spec = default_runtime_spec(service.id)
            service.network = "ioeb_app-network"
            service.port = "0.0.0.0:1021/TCP → 0.0.0.0:10021"
            service.volume = "/var/opt/gitlab/mnt/user → /appdata/aml/metaApp"
            if service.status == "default":
                service.status = "pre_release_unrated"
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return len(planned)
