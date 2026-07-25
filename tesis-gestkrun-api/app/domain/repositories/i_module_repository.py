from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.module import Module
from app.domain.value_objects import ModuleId, ProjectId


class IModuleRepository(ABC):
    @abstractmethod
    async def save(self, module: Module) -> None: ...

    @abstractmethod
    async def get_by_id(self, module_id: ModuleId) -> Module | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Module]: ...

    @abstractmethod
    async def delete(self, module_id: ModuleId) -> None: ...
