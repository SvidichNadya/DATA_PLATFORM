from fastapi import APIRouter, Depends, HTTPException, status
from asyncpg import Connection
import uuid
from typing import List

from app.database import get_db
from app.ingestion import schemas, crud

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post(
    "",
    response_model=schemas.IngestionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_ingestion(
    data: schemas.IngestionCreate,
    db: Connection = Depends(get_db),
):
    return await crud.create_ingestion(db, data)


@router.get(
    "/{ingestion_id}",
    response_model=schemas.IngestionRead,
)
async def read_ingestion(
    ingestion_id: uuid.UUID,
    db: Connection = Depends(get_db),
):
    record = await crud.get_ingestion(db, ingestion_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record


@router.get(
    "",
    response_model=List[schemas.IngestionRead],
)
async def list_ingestions(
    limit: int = 50,
    db: Connection = Depends(get_db),
):
    return await crud.list_ingestions(db, limit)
