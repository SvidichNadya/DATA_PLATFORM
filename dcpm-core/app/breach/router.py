from fastapi import APIRouter

router = APIRouter(prefix="/breach", tags=["Breach"])


@router.get("/example")
async def breach_example():
    return {
        "status": "ok",
        "module": "breach",
        "message": "stub endpoint"
    }
