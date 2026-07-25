from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities.message import Message
from app.domain.entities.user import User
from app.domain.enums import TipoMensaje
from app.domain.value_objects import ProjectId, TaskId, UserId
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.repositories.message_repository import MessageRepository

router = APIRouter(prefix="/projects/{project_id}/messages", tags=["messages"])


class SendMessageRequest(BaseModel):
    contenido: str
    tipo: str = "PROYECTO"
    task_id: str | None = None


async def _user_nombre(db: AsyncSession, user_id: UserId) -> str:
    result = await db.execute(select(UserModel.nombre).where(UserModel.id == str(user_id)))
    row = result.scalar_one_or_none()
    return row or str(user_id)[:8]


@router.post("")
async def send_message(
    project_id: str,
    body: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = MessageRepository(db)
    msg = Message.send(
        contenido=body.contenido,
        sender_id=current_user.id,
        tipo=TipoMensaje(body.tipo),
        proyecto_id=ProjectId(value=UUID(project_id)),
        task_id=TaskId(value=UUID(body.task_id)) if body.task_id else None,
    )
    await repo.save(msg)
    return {
        "id": str(msg.id),
        "contenido": msg.contenido,
        "sender_id": str(msg.sender_id),
        "sender_nombre": current_user.nombre,
        "tipo": msg.tipo.value,
        "fecha_envio": msg.fecha_envio.isoformat(),
    }


@router.get("")
async def list_messages(
    project_id: str,
    cursor: str | None = Query(None),
    limit: int = Query(50, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = MessageRepository(db)
    messages = await repo.list_by_project(
        ProjectId(value=UUID(project_id)), cursor=cursor, limit=limit
    )
    result = []
    for m in messages:
        nombre = await _user_nombre(db, m.sender_id)
        result.append({
            "id": str(m.id),
            "contenido": m.contenido,
            "sender_id": str(m.sender_id),
            "sender_nombre": nombre,
            "tipo": m.tipo.value,
            "fecha_envio": m.fecha_envio.isoformat(),
        })
    next_cursor = result[-1]["id"] if len(result) == limit else None
    return {"data": result, "next_cursor": next_cursor}
