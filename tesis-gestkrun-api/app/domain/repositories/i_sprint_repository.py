from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.sprint import Sprint
from app.domain.value_objects import ProjectId, SprintId


class ISprintRepository(ABC):
    @abstractmethod
    async def save(self, sprint: Sprint) -> None: ...

    @abstractmethod
    async def get_by_id(self, sprint_id: SprintId) -> Sprint | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Sprint]: ...

    @abstractmethod
    async def get_active_by_project(self, project_id: ProjectId) -> Sprint | None: ...

    @abstractmethod
    async def list_by_ids(self, sprint_ids: list[SprintId]) -> list[Sprint]: ...

    @abstractmethod
    async def delete(self, sprint_id: SprintId) -> None: ...
