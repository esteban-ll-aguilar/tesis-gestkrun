from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.value_objects import (
    EpicaId,
    EstimacionEsfuerzo,
    HistoriaUsuarioId,
    ModuleId,
    ProjectId,
)
from app.infrastructure.persistence.models.epica_model import EpicaModel
from app.infrastructure.persistence.models.historia_usuario_model import HistoriaUsuarioModel


class HistoriaUsuarioRepository(IHistoriaUsuarioRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, historia: HistoriaUsuario) -> None:
        model = HistoriaUsuarioModel(
            id=str(historia.id),
            epica_id=str(historia.epica_id),
            modulo_id=str(historia.modulo_id) if historia.modulo_id else None,
            titulo=historia.titulo,
            descripcion=historia.descripcion,
            criterios_aceptacion=historia.criterios_aceptacion,
            prioridad=historia.prioridad,
            estimacion=int(historia.estimacion),
            orden=historia.orden,
            deleted_at=historia.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, historia_id: HistoriaUsuarioId) -> HistoriaUsuario | None:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(HistoriaUsuarioModel.id == str(historia_id))
        )
        model = result.scalar_one_or_none()
        return _historia_from_model(model) if model else None

    async def list_by_epica(self, epica_id: EpicaId) -> list[HistoriaUsuario]:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(
                HistoriaUsuarioModel.epica_id == str(epica_id),
                HistoriaUsuarioModel.deleted_at.is_(None),
            ).order_by(HistoriaUsuarioModel.orden)
        )
        return [_historia_from_model(m) for m in result.scalars()]

    async def list_by_project(self, project_id: ProjectId) -> list[HistoriaUsuario]:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).join(
                EpicaModel, HistoriaUsuarioModel.epica_id == EpicaModel.id
            ).where(
                EpicaModel.project_id == str(project_id),
                HistoriaUsuarioModel.deleted_at.is_(None),
            ).order_by(EpicaModel.orden, HistoriaUsuarioModel.orden)
        )
        return [_historia_from_model(m) for m in result.scalars()]

    async def delete(self, historia_id: HistoriaUsuarioId) -> None:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(HistoriaUsuarioModel.id == str(historia_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _historia_from_model(model: HistoriaUsuarioModel) -> HistoriaUsuario:
    return HistoriaUsuario(
        id=HistoriaUsuarioId(value=UUID(model.id)),
        epica_id=EpicaId(value=UUID(model.epica_id)),
        modulo_id=ModuleId(value=UUID(model.modulo_id)) if model.modulo_id else None,
        titulo=model.titulo,
        descripcion=model.descripcion,
        criterios_aceptacion=model.criterios_aceptacion,
        prioridad=model.prioridad,
        estimacion=EstimacionEsfuerzo(model.estimacion),
        orden=model.orden,
        deleted_at=model.deleted_at,
    )
