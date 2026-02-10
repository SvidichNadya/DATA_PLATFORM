from fastapi import APIRouter

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.get("/example")
async def storage_example():
    return {
        "status": "ok",
        "module": "storage",
        "message": "stub endpoint"
    }
