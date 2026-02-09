from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import (
    wait_for_database,
    check_database_health,
    close_pool,
)

# Routers (пока example-заглушки, как у тебя сейчас)
from app.ingestion.router import router as ingestion_router
from app.classification.router import router as classification_router
from app.storage.router import router as storage_router
from app.audit.router import router as audit_router
from app.lifecycle.router import router as lifecycle_router
from app.rights.router import router as rights_router
from app.breach.router import router as breach_router
from app.security.router import router as security_router


# =========================
# FastAPI app
# =========================

app = FastAPI(
    title="DCPM Core API",
    version="0.1.0",
    description="MVP API for Data Collection & Processing Module (DCPM)",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


# =========================
# Startup / Shutdown
# =========================

@app.on_event("startup")
async def on_startup() -> None:
    """
    Application startup hook.
    Ensures database is reachable before serving requests.
    """
    await wait_for_database()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    Graceful shutdown.
    """
    await close_pool()


# =========================
# Health endpoint
# =========================

@app.get("/health", tags=["Health"])
async def health():
    db_ok = await check_database_health()

    if not db_ok:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "database": "unreachable",
            },
        )

    return {
        "status": "ok",
        "database": "reachable",
    }


# =========================
# Root
# =========================

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "DCPM Core API",
        "version": "0.1.0",
        "status": "running",
    }


# =========================
# Routers
# =========================

app.include_router(ingestion_router, prefix="/ingestion", tags=["Ingestion"])
app.include_router(classification_router, prefix="/classification", tags=["Classification"])
app.include_router(storage_router, prefix="/storage", tags=["Storage"])
app.include_router(audit_router, prefix="/audit", tags=["Audit"])
app.include_router(lifecycle_router, prefix="/lifecycle", tags=["Lifecycle"])
app.include_router(rights_router, prefix="/rights", tags=["Rights"])
app.include_router(breach_router, prefix="/breach", tags=["Breach"])
app.include_router(security_router, prefix="/security", tags=["Security"])
