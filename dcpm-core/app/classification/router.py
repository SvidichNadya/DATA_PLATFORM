from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection
from typing import List
import uuid

from app.classification import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/classification", tags=["Classification"])

@router.post("/classification", response_model=schemas.ClassificationRead)
async def create_classification(data: schemas.ClassificationCreate, db: Connection = Depends(get_db)):
    # Проверяем, что ingestion_id существует
    ingestion = await db.fetchrow(
        "SELECT ingestion_records_id FROM ingestion_records WHERE ingestion_records_id=$1",
        data.ingestion_id
    )
    if not ingestion:
        raise HTTPException(status_code=404, detail="Ingestion record not found")
    
    return await crud.create_classification(db, data)


@router.get("/classification/{ingestion_id}", response_model=List[schemas.ClassificationRead])
async def read_classification_by_ingestion(ingestion_id: uuid.UUID, db: Connection = Depends(get_db)):
    return await crud.get_classification_by_ingestion(db, ingestion_id)


@router.get("/classification", response_model=List[schemas.ClassificationRead])
async def list_classifications(limit: int = 50, db: Connection = Depends(get_db)):
    return await crud.list_classifications(db, limit)
