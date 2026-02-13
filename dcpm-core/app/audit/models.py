"""
SQL statements for audit module.
Contains ONLY raw SQL definitions.
"""

INSERT_AUDIT_SQL = """
INSERT INTO audit_logs (
    audit_logs_id,
    action,
    entity_type,
    entity_id,
    actor,
    metadata
)
VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb);
"""
