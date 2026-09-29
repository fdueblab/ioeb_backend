"""Owner-scoped MCP packaging workflow state."""

import json
import time

from app.extensions import db


class McpPackagingJob(db.Model):
    __tablename__ = "mcp_packaging_jobs"

    id = db.Column(db.String(36), primary_key=True)
    owner_id = db.Column(db.String(36), nullable=False, index=True)
    source_service_id = db.Column(db.String(36), nullable=True)
    source_name = db.Column(db.String(200), nullable=False, default="")
    source_path = db.Column(db.Text, nullable=False, default="")
    source_digest = db.Column(db.String(64), nullable=False, default="")
    spec_json = db.Column(db.Text, nullable=False, default="{}")
    candidates_json = db.Column(db.Text, nullable=False, default="[]")
    status = db.Column(db.String(32), nullable=False, default="draft")
    stage = db.Column(db.String(32), nullable=False, default="source")
    agent_task_id = db.Column(db.String(36), nullable=True)
    progress_text = db.Column(db.String(500), nullable=True)
    revision = db.Column(db.Integer, nullable=False, default=1)
    artifact_path = db.Column(db.Text, nullable=True)
    artifact_digest = db.Column(db.String(64), nullable=True)
    service_id = db.Column(db.String(36), nullable=True)
    verified_tools_json = db.Column(db.Text, nullable=False, default="[]")
    verified_at = db.Column(db.BigInteger, nullable=True)
    error = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: int(time.time() * 1000))

    def snapshot(self):
        return {
            "id": self.id, "sourceServiceId": self.source_service_id,
            "sourceName": self.source_name, "sourceDigest": self.source_digest,
            "spec": json.loads(self.spec_json or "{}"),
            "candidates": json.loads(self.candidates_json or "[]"),
            "status": self.status, "stage": self.stage, "revision": self.revision,
            "progressText": self.progress_text,
            "artifactReady": bool(self.artifact_path),
            "artifactDigest": self.artifact_digest, "serviceId": self.service_id,
            "verifiedTools": json.loads(self.verified_tools_json or "[]"),
            "verifiedAt": self.verified_at,
            "error": self.error, "updatedAt": self.updated_at,
        }
