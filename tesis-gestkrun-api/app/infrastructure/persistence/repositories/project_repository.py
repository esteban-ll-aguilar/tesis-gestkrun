from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.project import Project
from app.domain.repositories.i_project_repository import IProjectRepository
from app.domain.value_objects import ProjectId, UserId
from app.infrastructure.persistence.models.project_model import ProjectModel


class ProjectRepository(IProjectRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, project: Project) -> None:
        model = ProjectModel(
            id=str(project.id),
            nombre=project.nombre,
            descripcion=project.descripcion,
            estado=project.estado,
            fecha_inicio=project.fecha_inicio,
            owner_id=str(project.owner_id),
            deleted_at=project.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, project_id: ProjectId) -> Project | None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == str(project_id))
        )
        model = result.scalar_one_or_none()
        return _project_from_model(model) if model else None

    async def list_by_owner(self, owner_id: UserId) -> list[Project]:
        result = await self.session.execute(
            select(ProjectModel).where(
                ProjectModel.owner_id == str(owner_id),
                ProjectModel.deleted_at.is_(None),
            )
        )
        return [_project_from_model(m) for m in result.scalars()]

    async def list_all(self) -> list[Project]:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.deleted_at.is_(None))
        )
        return [_project_from_model(m) for m in result.scalars()]

    async def delete(self, project_id: ProjectId) -> None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == str(project_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _project_from_model(model: ProjectModel) -> Project:
    return Project(
        id=ProjectId(value=UUID(model.id)),
        nombre=model.nombre,
        descripcion=model.descripcion,
        estado=model.estado,
        fecha_inicio=model.fecha_inicio,
        owner_id=UserId(value=UUID(model.owner_id)),
        deleted_at=model.deleted_at,
    )
