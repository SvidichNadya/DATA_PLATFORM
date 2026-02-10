import uuid
import json
from typing import List
from asyncpg import Connection

from app.classification.schemas import ClassificationCreate, ClassificationRead
from app.audit.crud import write_audit_log
from app.audit.schemas import AuditLogCreate
from app.audit.constants import AuditAction

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

SELECT_BY_INGESTION_SQL = """
SELECT classification_id, ingestion_id, level, tags, created_at
FROM classification_records
WHERE ingestion_id = $1;
"""

SELECT_ALL_SQL = """
SELECT classification_id, ingestion_id, level, tags, created_at
FROM classification_records
ORDER BY created_at DESC
LIMIT $1;
"""


async def create_classification(db: Connection, data: ClassificationCreate) -> ClassificationRead:
    """
    Создание записи classification с аудит-логом.
    """
    async with db.transaction():
        record = await db.fetchrow(
            INSERT_SQL,
            uuid.uuid4(),
            data.ingestion_id,
            data.level,
            json.dumps(data.tags),
        )

        # Аудит
        await write_audit_log(
            db,
            AuditLogCreate(
                action=AuditAction.CLASSIFICATION_CREATED,
                entity_type="classification",
                entity_id=str(record["classification_id"]),
                actor="system",
                metadata={"ingestion_id": str(data.ingestion_id)},
            ),
        )

    return ClassificationRead(
        classification_id=record["classification_id"],
        ingestion_id=record["ingestion_id"],
        level=record["level"],
        tags=json.loads(record["tags"]),
        created_at=record["created_at"],
    )


async def get_classification_by_ingestion(
    db: Connection, ingestion_id: uuid.UUID
) -> List[ClassificationRead]:
    records = await db.fetch(SELECT_BY_INGESTION_SQL, ingestion_id)
    return [
        ClassificationRead(
            classification_id=r["classification_id"],
            ingestion_id=r["ingestion_id"],
            level=r["level"],
            tags=json.loads(r["tags"]),
            created_at=r["created_at"],
        )
        for r in records
    ]


async def list_classifications(db: Connection, limit: int = 50) -> List[ClassificationRead]:
    records = await db.fetch(SELECT_ALL_SQL, limit)
    return [
        ClassificationRead(
            classification_id=r["classification_id"],
            ingestion_id=r["ingestion_id"],
            level=r["level"],
            tags=json.loads(r["tags"]),
            created_at=r["created_at"],
        )
        for r in records
    ]
