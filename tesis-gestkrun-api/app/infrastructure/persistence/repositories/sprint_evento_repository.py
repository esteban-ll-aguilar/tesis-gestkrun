from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sprint_evento import SprintEvento
from app.domain.repositories.i_sprint_evento_repository import ISprintEventoRepository
from app.domain.value_objects import SprintEventoId, SprintId, UserId
from app.infrastructure.persistence.models.sprint_evento_model import SprintEventoModel


class SprintEventoRepository(ISprintEventoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, evento: SprintEvento) -> None:
        model = SprintEventoModel(
            id=str(evento.id),
            sprint_id=str(evento.sprint_id),
            tipo=evento.tipo,
            fecha=evento.fecha,
            notas=evento.notas,
            duracion_minutos=evento.duracion_minutos,
            created_by=str(evento.created_by),
        )
        self.session.add(model)

    async def list_by_sprint(self, sprint_id: SprintId) -> list[SprintEvento]:
        result = await self.session.execute(
            select(SprintEventoModel).where(
                SprintEventoModel.sprint_id == str(sprint_id)
            ).order_by(SprintEventoModel.fecha)
        )
        return [_sprint_evento_from_model(m) for m in result.scalars()]


def _sprint_evento_from_model(model: SprintEventoModel) -> SprintEvento:
    return SprintEvento(
        id=SprintEventoId(value=UUID(model.id)),
        sprint_id=SprintId(value=UUID(model.sprint_id)),
        tipo=model.tipo,
        fecha=model.fecha,
        notas=model.notas,
        duracion_minutos=model.duracion_minutos,
        created_by=UserId(value=UUID(model.created_by)),
    )
