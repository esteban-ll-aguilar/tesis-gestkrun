from __future__ import annotations

from datetime import UTC, datetime

from app.domain.repositories.i_project_repository import IProjectRepository
from app.domain.value_objects import ProjectId


class DeleteProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, project_id: ProjectId) -> bool:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return False
        project.deleted_at = datetime.now(UTC)
        await self._project_repo.save(project)
        return True
