from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.message import Message
from app.domain.repositories.i_message_repository import IMessageRepository
from app.domain.value_objects import MessageId, ProjectId, TaskId, UserId
from app.infrastructure.persistence.models.message_model import MessageModel


class MessageRepository(IMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: Message) -> None:
        model = MessageModel(
            id=str(message.id),
            proyecto_id=str(message.proyecto_id) if message.proyecto_id else None,
            task_id=str(message.task_id) if message.task_id else None,
            sender_id=str(message.sender_id),
            contenido=message.contenido,
            fecha_envio=message.fecha_envio,
            tipo=message.tipo,
        )
        self.session.add(model)

    async def list_by_project(
        self, project_id: ProjectId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]:
        query = select(MessageModel).where(
            MessageModel.proyecto_id == str(project_id)
        ).order_by(MessageModel.fecha_envio.desc()).limit(limit)
        if cursor:
            query = query.where(MessageModel.id < cursor)
        result = await self.session.execute(query)
        return [_message_from_model(m) for m in result.scalars()]

    async def list_by_task(
        self, task_id: TaskId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]:
        query = select(MessageModel).where(
            MessageModel.task_id == str(task_id)
        ).order_by(MessageModel.fecha_envio.desc()).limit(limit)
        if cursor:
            query = query.where(MessageModel.id < cursor)
        result = await self.session.execute(query)
        return [_message_from_model(m) for m in result.scalars()]


def _message_from_model(model: MessageModel) -> Message:
    return Message(
        id=MessageId(value=UUID(model.id)),
        proyecto_id=ProjectId(value=UUID(model.proyecto_id)) if model.proyecto_id else None,
        task_id=TaskId(value=UUID(model.task_id)) if model.task_id else None,
        sender_id=UserId(value=UUID(model.sender_id)),
        contenido=model.contenido,
        fecha_envio=model.fecha_envio,
        tipo=model.tipo,
    )
