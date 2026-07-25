from __future__ import annotations

from app.application.dto.backlog import SprintResult
from app.application.mappers.backlog_mapper import sprint_to_result
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.value_objects import ProjectId


class ListSprintsUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, project_id: ProjectId) -> list[SprintResult]:
        sprints = await self._repo.list_by_project(project_id)
        return [sprint_to_result(s) for s in sprints]
