from __future__ import annotations

from uuid import UUID

from sqlalchemy import func as sa_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.project_assignment import ProjectAssignment
from app.domain.repositories.i_project_assignment_repository import IProjectAssignmentRepository
from app.domain.value_objects import ProjectId, UserId
from app.infrastructure.persistence.models.project_assignment_model import ProjectAssignmentModel


class ProjectAssignmentRepository(IProjectAssignmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assignment: ProjectAssignment) -> None:
        model = ProjectAssignmentModel(
            id=str(assignment.id),
            project_id=str(assignment.project_id),
            user_id=str(assignment.user_id),
            rol=assignment.rol,
            deleted_at=assignment.deleted_at,
        )
        self.session.add(model)

    async def get_by_project_and_user(
        self, project_id: ProjectId, user_id: UserId,
    ) -> ProjectAssignment | None:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.user_id == str(user_id),
                ProjectAssignmentModel.deleted_at.is_(None),
            )
        )
        model = result.scalar_one_or_none()
        return _assignment_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[ProjectAssignment]:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.deleted_at.is_(None),
            )
        )
        return [_assignment_from_model(m) for m in result.scalars()]

    async def remove(self, project_id: ProjectId, user_id: UserId) -> None:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.user_id == str(user_id),
            )
        )
        model = result.scalar_one_or_none()
        if model:
            model.deleted_at = sa_func.now()


def _assignment_from_model(model: ProjectAssignmentModel) -> ProjectAssignment:
    return ProjectAssignment(
        id=model.id,
        project_id=ProjectId(value=UUID(model.project_id)),
        user_id=UserId(value=UUID(model.user_id)),
        rol=model.rol,
        deleted_at=model.deleted_at,
    )
