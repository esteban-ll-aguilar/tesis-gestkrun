from __future__ import annotations

from app.application.dto.projects import CreateProjectDTO, ProjectResult
from app.application.mappers.project_mapper import project_to_result
from app.domain.entities.project import Project
from app.domain.repositories.i_project_repository import IProjectRepository


class CreateProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, dto: CreateProjectDTO) -> ProjectResult:
        project = Project.create(dto.nombre, dto.descripcion, dto.owner_id)
        await self._project_repo.save(project)
        return project_to_result(project)
