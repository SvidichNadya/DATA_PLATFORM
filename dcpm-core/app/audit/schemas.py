from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Dict, Any


class AuditLogCreate(BaseModel):
    action: str = Field(..., examples=["INGESTION_CREATED"])
    entity_type: str = Field(..., examples=["ingestion"])
    entity_id: uuid.UUID
    actor: str = Field(..., examples=["system", "user:123"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditLogRead(AuditLogCreate):
    audit_id: uuid.UUID
    created_at: datetime
