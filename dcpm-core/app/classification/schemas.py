import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class ClassificationCreate(BaseModel):
    ingestion_id: uuid.UUID
    level: str
    tags: dict = Field(default_factory=dict)

class ClassificationRead(BaseModel):
    classification_id: uuid.UUID
    ingestion_id: uuid.UUID
    level: str
    tags: dict
    created_at: datetime
