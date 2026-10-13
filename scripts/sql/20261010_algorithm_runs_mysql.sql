-- Apply after backing up the production database, before deploying the backend.
-- Existing algorithm_artifacts columns are unchanged.
CREATE TABLE IF NOT EXISTS algorithm_runs (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    service_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    artifact_version INTEGER NOT NULL,
    status VARCHAR(24) NOT NULL,
    error_code VARCHAR(40) NULL,
    started_at BIGINT NOT NULL,
    finished_at BIGINT NULL,
    duration_ms INTEGER NULL,
    INDEX ix_algorithm_runs_service_id (service_id),
    INDEX ix_algorithm_runs_user_id (user_id),
    CONSTRAINT fk_algorithm_runs_service_id FOREIGN KEY (service_id) REFERENCES services(id)
);
