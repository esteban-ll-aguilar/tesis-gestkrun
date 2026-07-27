import asyncio
import sys
from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from structlog import get_logger

from app.core.config import settings
from app.infrastructure.auth.password_hasher import PasswordHasherService

logger = get_logger()

hasher = PasswordHasherService()

USERS = [
    {
        "nombre": "Super Admin",
        "email": "superadmin@admin.com",
        "password": "Test123!",
        "rol": "ADMIN",
    },
    {
        "nombre": "Product Owner",
        "email": "po@test.com",
        "password": "Test123!",
        "rol": "PRODUCT_OWNER",
    },
    {
        "nombre": "Scrum Master",
        "email": "sm@test.com",
        "password": "Test123!",
        "rol": "SCRUM_MASTER",
    },
    {
        "nombre": "Developer One",
        "email": "dev1@test.com",
        "password": "Test123!",
        "rol": "DEVELOPER",
    },
]


async def seed():
    engine = create_async_engine(settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        for user in USERS:
            result = await session.execute(
                text("SELECT id, rol FROM users WHERE email = :email"),
                {"email": user["email"]},
            )
            row = result.fetchone()
            if row:
                existing_id, existing_rol = row
                if existing_rol != user["rol"]:
                    await session.execute(
                        text("UPDATE users SET rol = :rol WHERE id = :id"),
                        {"rol": user["rol"], "id": existing_id},
                    )
                    logger.info("seed_update_role", email=user["email"], rol=user["rol"])
                password_hash = str(hasher.hash(user["password"]))
                await session.execute(
                    text("UPDATE users SET password_hash = :hash WHERE id = :id"),
                    {"hash": password_hash, "id": existing_id},
                )
                logger.info("seed_update_password", email=user["email"])
            else:
                import uuid
                password_hash = str(hasher.hash(user["password"]))
                await session.execute(
                    text("""
                        INSERT INTO users (id, nombre, email, password_hash, rol, fecha_registro)
                        VALUES (:id, :nombre, :email, :password_hash, :rol, :fecha_registro)
                    """),
                    {
                        "id": str(uuid.uuid4()),
                        "nombre": user["nombre"],
                        "email": user["email"],
                        "password_hash": password_hash,
                        "rol": user["rol"],
                        "fecha_registro": datetime.now(UTC),
                    },
                )
                logger.info("seed_create_user", email=user["email"])
        await session.commit()
    logger.info("seed_complete")
    sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(seed())
