"""Runnable metadata for a generated clinical algorithm."""

import datetime
import json

from app.extensions import db


class AlgorithmArtifact(db.Model):
    __tablename__ = "algorithm_artifacts"

    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), primary_key=True)
    version = db.Column(db.Integer, nullable=False, default=1)
    code_sha256 = db.Column(db.String(64), nullable=False)
    spec_json = db.Column(db.Text, nullable=False)
    smoke_input_json = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(24), nullable=False, default="draft")
    validation_error = db.Column(db.Text, nullable=True)
    validated_at = db.Column(db.BigInteger, nullable=True)
    source_json = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "serviceId": self.service_id,
            "version": self.version,
            "codeSha256": self.code_sha256,
            "spec": json.loads(self.spec_json),
            "status": self.status,
            "validationError": self.validation_error,
            "validatedAt": self.validated_at,
            "source": json.loads(self.source_json) if self.source_json else None,
            "smokeInput": json.loads(self.smoke_input_json) if self.smoke_input_json else None,
            "publicTrialEnabled": bool((json.loads(self.source_json) if self.source_json else {}).get("publicTrialEnabled")),
        }

    def mark_ready(self):
        self.status = "ready"
        self.validation_error = None
        self.validated_at = int(datetime.datetime.now().timestamp() * 1000)
