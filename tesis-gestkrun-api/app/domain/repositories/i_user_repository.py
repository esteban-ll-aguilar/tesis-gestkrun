from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.user import User
from app.domain.value_objects import UserId


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def list_all(self, include_deleted: bool = False) -> list[User]: ...

    @abstractmethod
    async def delete(self, user_id: UserId) -> None: ...
