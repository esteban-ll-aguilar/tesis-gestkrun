from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.task import Task
from app.domain.value_objects import HistoriaUsuarioId, SprintId, TaskId, UserId


class ITaskRepository(ABC):
    @abstractmethod
    async def save(self, task: Task) -> None: ...

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Task | None: ...

    @abstractmethod
    async def list_by_sprint(self, sprint_id: SprintId) -> list[Task]: ...

    @abstractmethod
    async def list_by_sprints(self, sprint_ids: list[SprintId]) -> list[Task]: ...

    @abstractmethod
    async def list_by_assigned_user(
        self, user_id: UserId, estado: str | None = None,
    ) -> list[Task]: ...

    @abstractmethod
    async def count_by_user_and_estado(self, user_id: UserId, estado: str) -> int: ...

    @abstractmethod
    async def list_by_historia_ids(
        self, historia_ids: list[HistoriaUsuarioId],
    ) -> list[Task]: ...

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None: ...
