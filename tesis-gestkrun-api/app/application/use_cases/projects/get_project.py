from __future__ import annotations

from app.application.dto.projects import ProjectResult
from app.application.mappers.project_mapper import project_to_result
from app.domain.repositories.i_project_repository import IProjectRepository
from app.domain.value_objects import ProjectId


class GetProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, project_id: ProjectId) -> ProjectResult | None:
        project = await self._project_repo.get_by_id(project_id)
        return project_to_result(project) if project else None
