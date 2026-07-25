from __future__ import annotations

from app.application.dto.projects import ProjectResult
from app.application.mappers.project_mapper import project_to_result
from app.domain.repositories.i_project_repository import IProjectRepository


class GetProjectsUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self) -> list[ProjectResult]:
        projects = await self._project_repo.list_all()
        return [project_to_result(p) for p in projects]
