from __future__ import annotations

from uuid import UUID

from app.application.dto.backlog import EpicaResult
from app.application.mappers.backlog_mapper import epica_to_result
from app.domain.entities.epica import Epica
from app.domain.enums import Prioridad
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.value_objects import ModuleId, ProjectId


class CreateEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(
        self, project_id: ProjectId, titulo: str, descripcion: str,
        prioridad: Prioridad, modulo_id: str | None = None,
    ) -> EpicaResult:
        max_orden = await self._repo.get_max_orden(project_id)
        mid = ModuleId(value=UUID(modulo_id)) if modulo_id else None
        epica = Epica.create(project_id, titulo, descripcion, prioridad, max_orden + 1, mid)
        await self._repo.save(epica)
        return epica_to_result(epica)
