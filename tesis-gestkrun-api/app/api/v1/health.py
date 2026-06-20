from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.api.dependencies import get_session
from app.core.config import settings

router = APIRouter()
logger = get_logger()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "gestkrun-api"}


@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_session)):  # noqa: B008
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error("database_connection_failed", error=str(e))
        return {"status": "error", "database": "disconnected"}


@router.get("/metrics")
async def metrics():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
    }
