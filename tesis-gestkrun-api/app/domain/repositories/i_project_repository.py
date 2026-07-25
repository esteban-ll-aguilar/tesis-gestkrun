from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.project import Project
from app.domain.value_objects import ProjectId, UserId


class IProjectRepository(ABC):
    @abstractmethod
    async def save(self, project: Project) -> None: ...

    @abstractmethod
    async def get_by_id(self, project_id: ProjectId) -> Project | None: ...

    @abstractmethod
    async def list_by_owner(self, owner_id: UserId) -> list[Project]: ...

    @abstractmethod
    async def list_all(self) -> list[Project]: ...

    @abstractmethod
    async def delete(self, project_id: ProjectId) -> None: ...
