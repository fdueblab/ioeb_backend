"""Canonical published meta-app configuration helpers."""

from __future__ import annotations

ARTIFACT_SCHEMA = "meta_app_artifact.v1"

STOPPABLE_STATUSES = frozenset({"pre_release_unrated", "pre_release_pending", "released", "deploying"})
DEPLOYABLE_STATUSES = frozenset({"not_deployed", "error"})
