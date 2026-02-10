from fastapi import APIRouter

router = APIRouter(prefix="/lifecycle", tags=["Lifecycle"])


@router.get("/example")
async def lifecycle_example():
    return {
        "status": "ok",
        "module": "lifecycle",
        "message": "stub endpoint"
    }
