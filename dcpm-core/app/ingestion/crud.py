import uuid
from typing import List
from asyncpg import Connection

from app.ingestion.schemas import IngestionCreate, IngestionRead


INSERT_SQL = """
INSERT INTO ingestion_records (
    ingestion_id,
    source,
    payload,
    classification
)
VALUES ($1, $2, $3::jsonb, $4::jsonb)
RETURNING ingestion_id, source, payload, classification, created_at;
"""

SELECT_BY_ID_SQL = """
SELECT
    ingestion_id,
    source,
    payload,
    classification,
    created_at
FROM ingestion_records
WHERE ingestion_id = $1;
"""

SELECT_LATEST_SQL = """
SELECT
    ingestion_id,
    source,
    payload,
    classification,
    created_at
FROM ingestion_records
ORDER BY created_at DESC
LIMIT $1;
"""


async def create_ingestion(
    db: Connection,
    data: IngestionCreate,
) -> IngestionRead:
    record = await db.fetchrow(
        INSERT_SQL,
        uuid.uuid4(),
        data.source,
        data.payload,
        data.classification,
    )
    return IngestionRead(**dict(record))


async def get_ingestion(
    db: Connection,
    ingestion_id: uuid.UUID,
) -> IngestionRead | None:
    record = await db.fetchrow(
        SELECT_BY_ID_SQL,
        ingestion_id,
    )
    if not record:
        return None
    return IngestionRead(**dict(record))


async def list_ingestions(
    db: Connection,
    limit: int = 50,
) -> List[IngestionRead]:
    records = await db.fetch(
        SELECT_LATEST_SQL,
        limit,
    )
    return [IngestionRead(**dict(r)) for r in records]
