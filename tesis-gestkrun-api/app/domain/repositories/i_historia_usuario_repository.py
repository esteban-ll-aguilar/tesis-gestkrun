from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.value_objects import EpicaId, HistoriaUsuarioId, ProjectId


class IHistoriaUsuarioRepository(ABC):
    @abstractmethod
    async def save(self, historia: HistoriaUsuario) -> None: ...

    @abstractmethod
    async def get_by_id(self, historia_id: HistoriaUsuarioId) -> HistoriaUsuario | None: ...

    @abstractmethod
    async def list_by_epica(self, epica_id: EpicaId) -> list[HistoriaUsuario]: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[HistoriaUsuario]: ...

    @abstractmethod
    async def delete(self, historia_id: HistoriaUsuarioId) -> None: ...
