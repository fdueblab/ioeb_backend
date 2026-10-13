"""Metadata for a clinical algorithm execution; patient inputs are not stored."""

from app.extensions import db


class AlgorithmRun(db.Model):
    __tablename__ = "algorithm_runs"

    id = db.Column(db.String(36), primary_key=True)
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False, index=True)
    user_id = db.Column(db.String(36), nullable=False, index=True)
    artifact_version = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(24), nullable=False)
    error_code = db.Column(db.String(40), nullable=True)
    started_at = db.Column(db.BigInteger, nullable=False)
    finished_at = db.Column(db.BigInteger, nullable=True)
    duration_ms = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "runId": self.id,
            "serviceId": self.service_id,
            "version": self.artifact_version,
            "status": self.status,
            "errorCode": self.error_code,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "durationMs": self.duration_ms,
        }
