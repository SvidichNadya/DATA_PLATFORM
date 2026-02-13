# SQL для CRUD операций на classification_records

SELECT_BY_ID_SQL = """
SELECT
    classification_id,
    ingestion_id,
    level,
    tags,
    created_at
FROM classification_records
WHERE classification_id = $1;
"""

SELECT_BY_INGESTION_SQL = """
SELECT
    classification_id,
    ingestion_id,
    level,
    tags,
    created_at
FROM classification_records
WHERE ingestion_id = $1
ORDER BY created_at DESC;
"""

INSERT_SQL = """
INSERT INTO classification_records (
    classification_id,
    ingestion_id,
    level,
    tags
)
VALUES ($1, $2, $3, $4::jsonb)
RETURNING classification_id, ingestion_id, level, tags, created_at;
"""
