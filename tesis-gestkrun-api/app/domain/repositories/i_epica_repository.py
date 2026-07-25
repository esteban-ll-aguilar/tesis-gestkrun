from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.epica import Epica
from app.domain.value_objects import EpicaId, ProjectId


class IEpicaRepository(ABC):
    @abstractmethod
    async def save(self, epica: Epica) -> None: ...

    @abstractmethod
    async def get_by_id(self, epica_id: EpicaId) -> Epica | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Epica]: ...

    @abstractmethod
    async def delete(self, epica_id: EpicaId) -> None: ...

    @abstractmethod
    async def get_max_orden(self, project_id: ProjectId) -> int: ...
