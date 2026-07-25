from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.message import Message
from app.domain.value_objects import ProjectId, TaskId


class IMessageRepository(ABC):
    @abstractmethod
    async def save(self, message: Message) -> None: ...

    @abstractmethod
    async def list_by_project(
        self, project_id: ProjectId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]: ...

    @abstractmethod
    async def list_by_task(
        self, task_id: TaskId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]: ...
