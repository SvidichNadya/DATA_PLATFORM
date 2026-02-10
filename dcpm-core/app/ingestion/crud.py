import uuid
import json
from typing import List
from asyncpg import Connection

from app.ingestion.schemas import IngestionCreate, IngestionRead
from app.audit.crud import write_audit_log
from app.audit.schemas import AuditLogCreate
from app.audit.constants import AuditAction

INSERT_SQL = """
INSERT INTO ingestion_records (
    ingestion_records_id,
    source,
    payload,
    classification
)
VALUES ($1, $2, $3::jsonb, $4::jsonb)
RETURNING ingestion_records_id, source, payload, classification, created_at;
"""

SELECT_BY_ID_SQL = """
SELECT
    ingestion_records_id,
    source,
    payload,
    classification,
    created_at
FROM ingestion_records
WHERE ingestion_records_id = $1;
"""

SELECT_LATEST_SQL = """
SELECT
    ingestion_records_id,
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
    """
    Создание записи ingestion с автоматическим аудит-логом.
    payload и classification конвертируются в JSON строку для Postgres.
    """
    async with db.transaction():
        record = await db.fetchrow(
            INSERT_SQL,
            uuid.uuid4(),
            data.source,
            json.dumps(data.payload),        # dict → JSON
            json.dumps(data.classification) # dict → JSON
        )

        # Запись аудит-лога
        await write_audit_log(
            db,
            AuditLogCreate(
                action=AuditAction.INGESTION_CREATED,
                entity_type="ingestion",
                entity_id=str(record["ingestion_records_id"]),
                actor="system",
                metadata={"source": data.source},
            ),
        )

    # Конвертируем JSON обратно в dict для Pydantic
    return IngestionRead(
        ingestion_id=record["ingestion_records_id"],
        source=record["source"],
        payload=json.loads(record["payload"]),
        classification=json.loads(record["classification"]),
        created_at=record["created_at"]
    )


async def get_ingestion(
    db: Connection,
    ingestion_id: uuid.UUID,
) -> IngestionRead | None:
    """
    Получение конкретной записи по ID.
    """
    record = await db.fetchrow(SELECT_BY_ID_SQL, ingestion_id)
    if not record:
        return None
    return IngestionRead(
        ingestion_id=record["ingestion_records_id"],
        source=record["source"],
        payload=json.loads(record["payload"]),
        classification=json.loads(record["classification"]),
        created_at=record["created_at"]
    )


async def list_ingestions(
    db: Connection,
    limit: int = 50,
) -> List[IngestionRead]:
    """
    Получение последних записей ingestion с ограничением.
    """
    records = await db.fetch(SELECT_LATEST_SQL, limit)
    result = []
    for r in records:
        result.append(
            IngestionRead(
                ingestion_id=r["ingestion_records_id"],
                source=r["source"],
                payload=json.loads(r["payload"]),
                classification=json.loads(r["classification"]),
                created_at=r["created_at"]
            )
        )
    return result
