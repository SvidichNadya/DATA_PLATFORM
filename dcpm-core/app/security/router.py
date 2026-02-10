from fastapi import APIRouter

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/example")
async def security_example():
    return {
        "status": "ok",
        "module": "security",
        "message": "stub endpoint"
    }
