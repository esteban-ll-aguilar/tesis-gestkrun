from __future__ import annotations

from uuid import UUID

from app.application.dto.backlog import HistoriaUsuarioResult
from app.application.mappers.backlog_mapper import historia_to_result
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.enums import Prioridad
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.value_objects import EpicaId, EstimacionEsfuerzo, ModuleId


class CreateHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(
        self, epica_id: EpicaId, titulo: str, descripcion: str,
        criterios_aceptacion: str, prioridad: Prioridad,
        estimacion: int, modulo_id: str | None = None,
    ) -> HistoriaUsuarioResult:
        hu = HistoriaUsuario.create(
            epica_id, titulo, descripcion, criterios_aceptacion,
            prioridad, EstimacionEsfuerzo(estimacion), 1,
            modulo_id=ModuleId(value=UUID(modulo_id)) if modulo_id else None,
        )
        await self._repo.save(hu)
        return historia_to_result(hu)
