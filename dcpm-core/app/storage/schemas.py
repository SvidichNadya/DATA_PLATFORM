from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class StorageCreate(BaseModel):
    ingestion_id: UUID
    classification_id: Optional[UUID] = None


class StorageRead(BaseModel):
    storage_id: UUID
    ingestion_id: UUID
    classification_id: Optional[UUID] = None
    normalized_payload: dict
    created_at: datetime

    class Config:
        from_attributes = True
