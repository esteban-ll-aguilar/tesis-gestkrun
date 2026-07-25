from __future__ import annotations

from datetime import datetime

from app.application.dto.backlog import SprintEventoResult
from app.application.mappers.backlog_mapper import evento_to_result
from app.domain.entities.sprint_evento import SprintEvento
from app.domain.enums import TipoEventoScrum
from app.domain.repositories.i_sprint_evento_repository import ISprintEventoRepository
from app.domain.value_objects import SprintEventoId, SprintId, UserId


class CreateSprintEventoUseCase:
    def __init__(self, repo: ISprintEventoRepository):
        self._repo = repo

    async def execute(
        self, sprint_id: SprintId, tipo: TipoEventoScrum, notas: str,
        duracion_minutos: int, created_by: UserId,
    ) -> SprintEventoResult:
        evento = SprintEvento(
            id=SprintEventoId.generate(),
            sprint_id=sprint_id,
            tipo=tipo,
            fecha=datetime.now(),
            notas=notas,
            duracion_minutos=duracion_minutos,
            created_by=created_by,
        )
        await self._repo.save(evento)
        return evento_to_result(evento)
