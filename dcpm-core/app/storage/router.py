from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from uuid import UUID

from app.database import get_db
from app.storage import crud, schemas

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("/storage", response_model=schemas.StorageRead)
async def create_storage_endpoint(data: schemas.StorageCreate, db=Depends(get_db)):
    try:
        return await crud.create_storage(db, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/storage/{storage_id}", response_model=schemas.StorageRead)
async def get_storage_endpoint(storage_id: UUID, db=Depends(get_db)):
    record = await crud.get_storage(db, storage_id)
    if not record:
        raise HTTPException(status_code=404, detail="Storage record not found")
    return record


@router.get("/storage", response_model=List[schemas.StorageRead])
async def list_storage_endpoint(limit: int = Query(50, ge=1, le=500), db=Depends(get_db)):
    return await crud.list_storage(db, limit)
