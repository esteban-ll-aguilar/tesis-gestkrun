from __future__ import annotations

from app.application.dto.backlog import SprintEventoResult
from app.application.mappers.backlog_mapper import evento_to_result
from app.domain.repositories.i_sprint_evento_repository import ISprintEventoRepository
from app.domain.value_objects import SprintId


class ListSprintEventosUseCase:
    def __init__(self, repo: ISprintEventoRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> list[SprintEventoResult]:
        eventos = await self._repo.list_by_sprint(sprint_id)
        return [evento_to_result(e) for e in eventos]
