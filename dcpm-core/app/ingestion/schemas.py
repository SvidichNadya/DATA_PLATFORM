from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime
import uuid


class IngestionCreate(BaseModel):
    source: str = Field(..., examples=["api", "webhook", "file"])
    payload: Dict[str, Any]
    classification: Dict[str, Any]


class IngestionRead(BaseModel):
    ingestion_id: uuid.UUID
    source: str
    payload: Dict[str, Any]
    classification: Dict[str, Any]
    created_at: datetime

    model_config = {
        "from_attributes": True  # Pydantic v2 аналог orm_mode
    }
