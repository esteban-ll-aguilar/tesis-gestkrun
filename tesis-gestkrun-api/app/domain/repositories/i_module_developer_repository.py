from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.module_developer import ModuleDeveloper
from app.domain.value_objects import ModuleId, ProjectId, UserId


class IModuleDeveloperRepository(ABC):
    @abstractmethod
    async def save(self, assignment: ModuleDeveloper) -> None: ...

    @abstractmethod
    async def list_by_module(self, module_id: ModuleId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def list_by_user(self, user_id: UserId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def remove(self, module_id: ModuleId, user_id: UserId) -> None: ...
