from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sprint import Sprint
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.value_objects import ProjectId, SprintId
from app.infrastructure.persistence.models.sprint_model import SprintModel


class SprintRepository(ISprintRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, sprint: Sprint) -> None:
        model = SprintModel(
            id=str(sprint.id),
            project_id=str(sprint.project_id),
            nombre=sprint.nombre,
            objetivo=sprint.objetivo,
            duracion_dias=sprint.duracion_dias,
            fecha_inicio=sprint.fecha_inicio,
            fecha_fin=sprint.fecha_fin,
            estado=sprint.estado,
            meeting_link=sprint.meeting_link,
            deleted_at=sprint.deleted_at,
        )
        await self.session.merge(model)

    async def get_by_id(self, sprint_id: SprintId) -> Sprint | None:
        result = await self.session.execute(
            select(SprintModel).where(SprintModel.id == str(sprint_id))
        )
        model = result.scalar_one_or_none()
        return _sprint_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[Sprint]:
        result = await self.session.execute(
            select(SprintModel).where(
                SprintModel.project_id == str(project_id),
                SprintModel.deleted_at.is_(None),
            ).order_by(SprintModel.fecha_inicio.desc())
        )
        return [_sprint_from_model(m) for m in result.scalars()]

    async def list_by_ids(self, sprint_ids: list[SprintId]) -> list[Sprint]:
        ids = [str(s) for s in sprint_ids]
        result = await self.session.execute(
            select(SprintModel).where(SprintModel.id.in_(ids))
        )
        return [_sprint_from_model(m) for m in result.scalars()]

    async def get_active_by_project(self, project_id: ProjectId) -> Sprint | None:
        from app.domain.enums import EstadoSprint
        result = await self.session.execute(
            select(SprintModel).where(
                SprintModel.project_id == str(project_id),
                SprintModel.estado == EstadoSprint.EN_EJECUCION,
                SprintModel.deleted_at.is_(None),
            )
        )
        model = result.scalar_one_or_none()
        return _sprint_from_model(model) if model else None

    async def delete(self, sprint_id: SprintId) -> None:
        result = await self.session.execute(
            select(SprintModel).where(SprintModel.id == str(sprint_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _sprint_from_model(model: SprintModel) -> Sprint:
    return Sprint(
        id=SprintId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        nombre=model.nombre,
        objetivo=model.objetivo,
        duracion_dias=model.duracion_dias,
        fecha_inicio=model.fecha_inicio,
        fecha_fin=model.fecha_fin,
        estado=model.estado,
        meeting_link=model.meeting_link,
        deleted_at=model.deleted_at,
    )
