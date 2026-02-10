from fastapi import APIRouter

router = APIRouter(prefix="/config", tags=["Config"])


@router.get("/example")
async def config_example():
    return {
        "status": "ok",
        "module": "config",
        "message": "stub endpoint"
    }
