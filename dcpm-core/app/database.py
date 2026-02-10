import os
import asyncio
import asyncpg
from typing import Optional, AsyncGenerator

# =========================
# Database configuration
# =========================

DB_USER = os.getenv("POSTGRES_USER", "dcpm_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dcpm_pass")
DB_NAME = os.getenv("POSTGRES_DB", "dcpm_db")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# =========================
# Connection pool
# =========================

_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """
    Returns a global asyncpg pool. Creates it if it does not exist.
    """
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=1,
            max_size=10,
        )
    return _pool


async def close_pool() -> None:
    """
    Gracefully closes the global pool.
    """
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


# =========================
# FastAPI dependency
# =========================

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency.
    Yields a single DB connection from the pool.
    """
    pool = await get_pool()
    async with pool.acquire() as connection:
        yield connection


# =========================
# Startup wait logic
# =========================

async def wait_for_database(
    retries: int = 10,
    delay_seconds: int = 2,
) -> None:
    """
    Waits for the database to become available at startup.
    Retries a number of times with delay.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            pool = await get_pool()
            async with pool.acquire() as conn:
                await conn.execute("SELECT 1;")
            print("✅ Database is reachable")
            return
        except Exception as exc:
            last_error = exc
            print(f"⏳ Waiting for database (attempt {attempt}/{retries})...")
            await asyncio.sleep(delay_seconds)

    raise RuntimeError("❌ Database is unreachable after retries") from last_error


# =========================
# Health check
# =========================

async def check_database_health() -> bool:
    """
    Checks if the database is reachable using the pool.
    Returns True if healthy, False otherwise.
    """
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1;")
        return True
    except Exception:
        return False
