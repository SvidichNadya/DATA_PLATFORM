import uuid
import json
from asyncpg import Connection
from app.audit.schemas import AuditLogCreate

# SQL-запрос с явным ::jsonb для actor и metadata
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


async def write_audit_log(
    db: Connection,
    audit: AuditLogCreate,
) -> None:
    """
    Writes immutable audit log entry.
    Must be called INSIDE transaction.
    Serializes actor and metadata to JSON before writing to DB.
    """
    # Преобразуем dict -> JSON строка
    actor_json = json.dumps(audit.actor) if audit.actor else None
    metadata_json = json.dumps(audit.metadata) if audit.metadata else None

    await db.execute(
        INSERT_AUDIT_SQL,
        uuid.uuid4(),
        audit.action,
        audit.entity_type,
        audit.entity_id,
        actor_json,
        metadata_json,
    )
