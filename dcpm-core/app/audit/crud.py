"""
CRUD logic for audit module.
Responsible ONLY for writing immutable audit records.
"""

import uuid
import json
from asyncpg import Connection

from app.audit.schemas import AuditLogCreate
from app.audit.models import INSERT_AUDIT_SQL


async def write_audit_log(
    db: Connection,
    audit: AuditLogCreate,
) -> None:
    """
    Writes immutable audit log entry.

    IMPORTANT:
    - Must be called INSIDE an active DB transaction.
    - Serializes actor and metadata to JSON before writing.
    """

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
