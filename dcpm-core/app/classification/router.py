from fastapi import APIRouter

router = APIRouter(prefix="/classification", tags=["Classification"])


@router.get("/example")
async def classification_example():
    return {
        "status": "ok",
        "module": "classification",
        "message": "stub endpoint"
    }
