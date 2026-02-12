# Для asyncpg мы будем использовать чистый SQL, поэтому моделей ORM нет.
# Здесь можно хранить SQL-запросы для CRUD.
STORAGE_INSERT_SQL = """
INSERT INTO storage_records (
    storage_records_id,
    ingestion_id,
    classification_id,
    normalized_payload
)
VALUES ($1, $2, $3, $4::jsonb)
RETURNING storage_records_id, ingestion_id, classification_id, normalized_payload, created_at;
"""

STORAGE_SELECT_BY_ID_SQL = """
SELECT
    storage_records_id,
    ingestion_id,
    classification_id,
    normalized_payload,
    created_at
FROM storage_records
WHERE storage_records_id = $1;
"""

STORAGE_SELECT_LATEST_SQL = """
SELECT
    storage_records_id,
    ingestion_id,
    classification_id,
    normalized_payload,
    created_at
FROM storage_records
ORDER BY created_at DESC
LIMIT $1;
"""
