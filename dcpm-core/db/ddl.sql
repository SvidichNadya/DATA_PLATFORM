-- =============================================
-- Initial schema for DCPM MVP (v1.1)
-- =============================================

-- ----------------------------
-- 1. Ingestion: raw incoming data
-- ----------------------------
CREATE TABLE IF NOT EXISTS ingestion_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ----------------------------
-- 2. Classification: data classification
-- ----------------------------
CREATE TABLE IF NOT EXISTS classification_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingestion_id UUID NOT NULL REFERENCES ingestion_records(id) ON DELETE CASCADE,
    classification JSONB NOT NULL,
    classified_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ----------------------------
-- 3. Audit logs: logging actions
-- ----------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action VARCHAR(255) NOT NULL,
    actor VARCHAR(255) NULL,
    target_id UUID NULL,
    details JSONB NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ----------------------------
-- 4. Lifecycle events: data lifecycle management
-- ----------------------------
CREATE TABLE IF NOT EXISTS lifecycle_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingestion_id UUID NOT NULL REFERENCES ingestion_records(id) ON DELETE CASCADE,
    event_type VARCHAR(255) NOT NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    executed_at TIMESTAMPTZ NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    details JSONB NULL
);

-- ----------------------------
-- 5. Rights requests: user requests (delete/export)
-- ----------------------------
CREATE TABLE IF NOT EXISTS rights_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    request_type VARCHAR(50) NOT NULL, -- e.g., 'deletion', 'portability'
    target_id UUID NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ NULL
);

-- ----------------------------
-- 6. Breach events: security incidents
-- ----------------------------
CREATE TABLE IF NOT EXISTS breach_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL DEFAULT 'medium',
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ NULL,
    details JSONB NULL
);

-- ----------------------------
-- 7. Security events
-- ----------------------------
CREATE TABLE IF NOT EXISTS security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(255) NOT NULL,
    actor VARCHAR(255) NULL,
    target_id UUID NULL,
    details JSONB NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ----------------------------
-- Indexes
-- ----------------------------
CREATE INDEX IF NOT EXISTS idx_ingestion_created_at ON ingestion_records(created_at);
CREATE INDEX IF NOT EXISTS idx_classification_ingestion_id ON classification_records(ingestion_id);
CREATE INDEX IF NOT EXISTS idx_lifecycle_ingestion_id ON lifecycle_events(ingestion_id);
CREATE INDEX IF NOT EXISTS idx_rights_user_id ON rights_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_breach_severity ON breach_events(severity);
CREATE INDEX IF NOT EXISTS idx_security_event_type ON security_events(event_type);

-- =============================================
-- All tables ready for MVP
-- =============================================
