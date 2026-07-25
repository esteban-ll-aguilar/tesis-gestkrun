from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.i_user_repository import IUserRepository
from app.domain.value_objects import Email, PasswordHash, UserId
from app.infrastructure.persistence.models.user_model import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        model = UserModel(
            id=str(user.id),
            nombre=user.nombre,
            email=str(user.email),
            password_hash=str(user.password_hash),
            rol=user.rol,
            fecha_registro=user.fecha_registro,
            deleted_at=user.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, user_id: UserId) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == str(user_id))
        )
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def list_all(self, include_deleted: bool = False) -> list[User]:
        query = select(UserModel)
        if not include_deleted:
            query = query.where(UserModel.deleted_at.is_(None))
        result = await self.session.execute(query)
        return [_user_from_model(m) for m in result.scalars()]

    async def delete(self, user_id: UserId) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == str(user_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _user_from_model(model: UserModel) -> User:
    return User(
        id=UserId(value=UUID(model.id)),
        nombre=model.nombre,
        email=Email(model.email),
        password_hash=PasswordHash(model.password_hash),
        rol=model.rol,
        fecha_registro=model.fecha_registro,
        deleted_at=model.deleted_at,
    )
