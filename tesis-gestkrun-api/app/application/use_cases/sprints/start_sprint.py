from __future__ import annotations

from app.application.dto.backlog import SprintResult
from app.application.mappers.backlog_mapper import sprint_to_result
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.value_objects import SprintId


class StartSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> SprintResult:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            raise ValueError("Sprint not found")
        sprint.start()
        await self._repo.save(sprint)
        return sprint_to_result(sprint)
