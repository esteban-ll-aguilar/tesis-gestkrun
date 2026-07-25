from __future__ import annotations

from uuid import UUID

from app.application.dto.backlog import EpicaResult
from app.application.mappers.backlog_mapper import epica_to_result
from app.domain.enums import Prioridad
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.value_objects import EpicaId, ModuleId


class UpdateEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(
        self, epica_id: EpicaId, titulo: str | None = None,
        descripcion: str | None = None, prioridad: Prioridad | None = None,
        modulo_id: str | None = None,
    ) -> EpicaResult | None:
        epica = await self._repo.get_by_id(epica_id)
        if not epica:
            return None
        if titulo is not None:
            epica.titulo = titulo
        if descripcion is not None:
            epica.descripcion = descripcion
        if prioridad is not None:
            epica.prioridad = prioridad
        if modulo_id is not None:
            epica.modulo_id = ModuleId(value=UUID(modulo_id)) if modulo_id else None
        await self._repo.save(epica)
        return epica_to_result(epica)
