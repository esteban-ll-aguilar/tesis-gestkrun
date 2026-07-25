from __future__ import annotations

from app.application.dto.backlog import EpicaResult
from app.application.mappers.backlog_mapper import epica_to_result
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.value_objects import ProjectId


class ListEpicasUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(self, project_id: ProjectId) -> list[EpicaResult]:
        epicas = await self._repo.list_by_project(project_id)
        return [epica_to_result(e) for e in epicas]
