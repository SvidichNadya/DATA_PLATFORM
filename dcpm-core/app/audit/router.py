from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/example")
async def audit_example():
    return {
        "status": "ok",
        "module": "audit",
        "message": "stub endpoint"
    }
