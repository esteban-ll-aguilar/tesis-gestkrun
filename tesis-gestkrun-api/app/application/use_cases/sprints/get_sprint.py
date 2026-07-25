from __future__ import annotations

from app.application.dto.backlog import SprintResult
from app.application.mappers.backlog_mapper import sprint_to_result
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.value_objects import SprintId


class GetSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> SprintResult | None:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            return None
        return sprint_to_result(sprint)
