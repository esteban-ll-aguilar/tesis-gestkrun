from __future__ import annotations

from app.domain.entities.user import User
from app.domain.repositories.i_user_repository import IUserRepository
from app.domain.value_objects import Email


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def execute(self, nombre: str, email: str, password_hash: str) -> User:
        domain_user = User.register(nombre, Email(email), password_hash)
        await self._user_repo.save(domain_user)
        return domain_user
