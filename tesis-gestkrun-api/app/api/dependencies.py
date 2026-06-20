from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.enums import Rol
from app.infrastructure.auth.jwt_provider import JWTProvider
from app.infrastructure.persistence.repositories import UserRepository

jwt_provider = JWTProvider()


async def get_session() -> AsyncSession:
    async for session in get_db():
        yield session


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_session),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ")[1]
    user_id = jwt_provider.get_user_id_from_token(token)

    if not user_id or not jwt_provider.is_access_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_role(rol: Rol):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.rol != rol and current_user.rol != Rol.ADMIN:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker


def require_any_role(*roles: Rol):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.rol not in roles and current_user.rol != Rol.ADMIN:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker
