from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import (
    wait_for_database,
    check_database_health,
    close_pool,
)

# Routers
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
    Initializes connection pool.
    """
    await wait_for_database()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    Graceful shutdown: closes database pool.
    """
    await close_pool()


# =========================
# Health endpoint
# =========================

@app.get("/health", tags=["Health"])
async def health():
    """
    Returns service health including DB connectivity.
    """
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
# Root endpoint
# =========================

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "DCPM Core API",
        "version": "0.1.0",
        "status": "running",
    }


# =========================
# Routers registration
# =========================

app.include_router(ingestion_router)
app.include_router(classification_router)
app.include_router(storage_router)
app.include_router(audit_router)
app.include_router(lifecycle_router)
app.include_router(rights_router)
app.include_router(breach_router)
app.include_router(security_router)
