from __future__ import annotations

from datetime import date

from app.application.dto.backlog import SprintResult
from app.application.mappers.backlog_mapper import sprint_to_result
from app.domain.entities.sprint import Sprint
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.value_objects import ProjectId


class PlanSprintUseCase:
    def __init__(self, sprint_repo: ISprintRepository):
        self._sprint_repo = sprint_repo

    async def execute(
        self, project_id: ProjectId, nombre: str, objetivo: str,
        duracion_dias: int, fecha_inicio: date, meeting_link: str = "",
    ) -> SprintResult:
        sprint = Sprint.plan(
            project_id, nombre, objetivo, duracion_dias, fecha_inicio, meeting_link,
        )
        await self._sprint_repo.save(sprint)
        return sprint_to_result(sprint)
