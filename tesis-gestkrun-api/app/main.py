from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from structlog import get_logger

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException, exception_handler
from app.core.logging import setup_logging
from app.core.rate_limiter import limiter
from app.infrastructure.persistence.models import Base
from seed import seed

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("application_start", environment=settings.environment)

    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("""
            ALTER TABLE epicas ADD COLUMN IF NOT EXISTS modulo_id VARCHAR(36) REFERENCES modules(id)
        """))
    await engine.dispose()
    logger.info("database_tables_ready")

    try:
        logger.info("seed_starting")
        await seed()
        logger.info("seed_completed")
    except Exception as e:
        logger.error("seed_failed", error=str(e))
    yield
    logger.info("application_shutdown")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, exception_handler)
app.include_router(api_router)
