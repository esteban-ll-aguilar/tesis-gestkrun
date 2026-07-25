from __future__ import annotations

from uuid import UUID

from app.application.dto.backlog import HistoriaUsuarioResult
from app.application.mappers.backlog_mapper import historia_to_result
from app.domain.enums import Prioridad
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.value_objects import EstimacionEsfuerzo, HistoriaUsuarioId, ModuleId


class UpdateHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(
        self, historia_id: HistoriaUsuarioId, titulo: str | None = None,
        descripcion: str | None = None, criterios_aceptacion: str | None = None,
        prioridad: Prioridad | None = None, estimacion: int | None = None,
        modulo_id: str | None = None,
    ) -> HistoriaUsuarioResult | None:
        hu = await self._repo.get_by_id(historia_id)
        if not hu:
            return None
        if titulo is not None:
            hu.titulo = titulo
        if descripcion is not None:
            hu.descripcion = descripcion
        if criterios_aceptacion is not None:
            hu.criterios_aceptacion = criterios_aceptacion
        if prioridad is not None:
            hu.prioridad = prioridad
        if estimacion is not None:
            hu.estimacion = EstimacionEsfuerzo(estimacion)
        if modulo_id is not None:
            hu.modulo_id = ModuleId(value=UUID(modulo_id))
        await self._repo.save(hu)
        return historia_to_result(hu)
