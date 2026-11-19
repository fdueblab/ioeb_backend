"""Durable, owner-scoped state for creating a clinical algorithm."""

import json
import time

from sqlalchemy.dialects.mysql import LONGTEXT

from app.extensions import db


class ClinicalCreationJob(db.Model):
    __tablename__ = "clinical_creation_jobs"

    id = db.Column(db.String(36), primary_key=True)
    owner_id = db.Column(db.String(36), nullable=False, index=True)
    mode = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(24), nullable=False, default="draft")
    name = db.Column(db.String(100), nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")
    notes = db.Column(db.Text, nullable=False, default="")
    messages_json = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=False, default="[]")
    intake_json = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=False, default="{}")
    reference_name = db.Column(db.String(255), nullable=False, default="")
    reference_path = db.Column(db.Text, nullable=False, default="")
    reference_preview = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=False, default="")
    reference_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    progress_step = db.Column(db.Integer, nullable=False, default=0)
    progress_text = db.Column(db.String(500), nullable=False, default="")
    result_json = db.Column(db.Text().with_variant(LONGTEXT, "mysql"), nullable=True)
    error = db.Column(db.Text, nullable=True)
    service_id = db.Column(db.String(36), nullable=True)
    run_id = db.Column(db.String(36), nullable=True)
    heartbeat_at = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time() * 1000))
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time() * 1000))

    def snapshot(self, include_result=True):
        intake = json.loads(self.intake_json or "{}")
        if isinstance(intake.get("execution"), dict):
            intake["execution"].pop("resume_token", None)
        return {
            "id": self.id, "mode": self.mode, "status": self.status,
            "name": self.name, "description": self.description, "notes": self.notes,
            "departmentId": (intake.get("catalog") or {}).get("departmentId", ""),
            "messages": json.loads(self.messages_json or "[]"),
            "intake": intake,
            "referenceName": self.reference_name,
            "referencePreview": self.reference_preview,
            "referenceReviewed": self.reference_reviewed,
            "progressStep": self.progress_step, "progressText": self.progress_text,
            "result": json.loads(self.result_json) if include_result and self.result_json else None,
            "error": self.error, "serviceId": self.service_id,
            "createdAt": self.created_at, "updatedAt": self.updated_at,
        }
