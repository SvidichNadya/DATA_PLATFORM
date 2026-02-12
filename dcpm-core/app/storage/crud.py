import uuid
import json
from typing import List
from asyncpg import Connection

from app.storage.schemas import StorageCreate, StorageRead
from app.storage.models import STORAGE_INSERT_SQL, STORAGE_SELECT_BY_ID_SQL, STORAGE_SELECT_LATEST_SQL
from app.ingestion.crud import get_ingestion
from app.classification.crud import get_classification
from app.audit.crud import write_audit_log
from app.audit.schemas import AuditLogCreate
from app.audit.constants import AuditAction


async def create_storage(db: Connection, data: StorageCreate) -> StorageRead:
    """
    Создание записи storage с audit-логом.
    normalized_payload формируется на основе ingestion.payload.
    """
    # Получаем ingestion для нормализации
    ingestion = await get_ingestion(db, data.ingestion_id)
    if not ingestion:
        raise ValueError(f"Ingestion {data.ingestion_id} not found")

    # Опционально проверяем classification
    if data.classification_id:
        classification = await get_classification(db, data.classification_id)
        if not classification:
            raise ValueError(f"Classification {data.classification_id} not found")

    normalized_payload = ingestion.payload  # MVP: просто копируем

    async with db.transaction():
        record = await db.fetchrow(
            STORAGE_INSERT_SQL,
            uuid.uuid4(),
            data.ingestion_id,
            data.classification_id,
            json.dumps(normalized_payload)
        )

        # Audit лог
        await write_audit_log(
            db,
            AuditLogCreate(
                action=AuditAction.STORAGE_CREATED,
                entity_type="storage",
                entity_id=str(record["storage_records_id"]),
                actor="system",
                metadata={"ingestion_id": str(data.ingestion_id)},
            ),
        )

    return StorageRead(
        storage_id=record["storage_records_id"],
        ingestion_id=record["ingestion_id"],
        classification_id=record["classification_id"],
        normalized_payload=json.loads(record["normalized_payload"]),
        created_at=record["created_at"]
    )


async def get_storage(db: Connection, storage_id: uuid.UUID) -> StorageRead | None:
    record = await db.fetchrow(STORAGE_SELECT_BY_ID_SQL, storage_id)
    if not record:
        return None
    return StorageRead(
        storage_id=record["storage_records_id"],
        ingestion_id=record["ingestion_id"],
        classification_id=record["classification_id"],
        normalized_payload=json.loads(record["normalized_payload"]),
        created_at=record["created_at"]
    )


async def list_storage(db: Connection, limit: int = 50) -> List[StorageRead]:
    records = await db.fetch(STORAGE_SELECT_LATEST_SQL, limit)
    result = []
    for r in records:
        result.append(
            StorageRead(
                storage_id=r["storage_records_id"],
                ingestion_id=r["ingestion_id"],
                classification_id=r["classification_id"],
                normalized_payload=json.loads(r["normalized_payload"]),
                created_at=r["created_at"]
            )
        )
    return result
