from fastapi import APIRouter

router = APIRouter(prefix="/rights", tags=["Rights"])


@router.get("/example")
async def rights_example():
    return {
        "status": "ok",
        "module": "rights",
        "message": "stub endpoint"
    }
