from __future__ import annotations

from typing import Any

from app.domain.entities.user import User
from app.domain.repositories.i_user_repository import IUserRepository


class AuthenticateUserUseCase:
    def __init__(self, user_repo: IUserRepository, password_hasher: Any):
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> User | None:
        user = await self._user_repo.get_by_email(email)
        if not user:
            return None
        if not self._password_hasher.verify(user.password_hash, password):
            return None
        return user
