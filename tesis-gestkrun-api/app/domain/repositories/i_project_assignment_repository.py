from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.project_assignment import ProjectAssignment
from app.domain.value_objects import ProjectId, UserId


class IProjectAssignmentRepository(ABC):
    @abstractmethod
    async def save(self, assignment: ProjectAssignment) -> None: ...

    @abstractmethod
    async def get_by_project_and_user(
        self, project_id: ProjectId, user_id: UserId,
    ) -> ProjectAssignment | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[ProjectAssignment]: ...

    @abstractmethod
    async def remove(self, project_id: ProjectId, user_id: UserId) -> None: ...
