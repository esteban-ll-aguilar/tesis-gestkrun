from __future__ import annotations

from uuid import UUID

from sqlalchemy import func as sa_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.epica import Epica
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.value_objects import EpicaId, ModuleId, ProjectId
from app.infrastructure.persistence.models.epica_model import EpicaModel


class EpicaRepository(IEpicaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, epica: Epica) -> None:
        model = EpicaModel(
            id=str(epica.id),
            project_id=str(epica.project_id),
            titulo=epica.titulo,
            descripcion=epica.descripcion,
            prioridad=epica.prioridad,
            estado=epica.estado,
            orden=epica.orden,
            modulo_id=str(epica.modulo_id) if epica.modulo_id else None,
            deleted_at=epica.deleted_at,
        )
        await self.session.merge(model)

    async def get_by_id(self, epica_id: EpicaId) -> Epica | None:
        result = await self.session.execute(
            select(EpicaModel).where(EpicaModel.id == str(epica_id))
        )
        model = result.scalar_one_or_none()
        return _epica_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[Epica]:
        result = await self.session.execute(
            select(EpicaModel).where(
                EpicaModel.project_id == str(project_id),
                EpicaModel.deleted_at.is_(None),
            ).order_by(EpicaModel.orden)
        )
        return [_epica_from_model(m) for m in result.scalars()]

    async def delete(self, epica_id: EpicaId) -> None:
        result = await self.session.execute(
            select(EpicaModel).where(EpicaModel.id == str(epica_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)

    async def get_max_orden(self, project_id: ProjectId) -> int:
        result = await self.session.execute(
            select(sa_func.max(EpicaModel.orden)).where(
                EpicaModel.project_id == str(project_id)
            )
        )
        return result.scalar() or 0


def _epica_from_model(model: EpicaModel) -> Epica:
    return Epica(
        id=EpicaId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        titulo=model.titulo,
        descripcion=model.descripcion,
        prioridad=model.prioridad,
        estado=model.estado,
        orden=model.orden,
        modulo_id=ModuleId(value=UUID(model.modulo_id)) if model.modulo_id else None,
        deleted_at=model.deleted_at,
    )
