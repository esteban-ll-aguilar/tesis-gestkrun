from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import TipoMensaje
from app.domain.events import DomainEvent, MessageSent
from app.domain.value_objects import MessageId, ProjectId, TaskId, UserId


@dataclass
class Message:
    id: MessageId
    proyecto_id: ProjectId | None
    task_id: TaskId | None
    sender_id: UserId
    contenido: str
    fecha_envio: datetime
    tipo: TipoMensaje

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def send(
        contenido: str,
        sender_id: UserId,
        tipo: TipoMensaje,
        proyecto_id: ProjectId | None = None,
        task_id: TaskId | None = None,
    ) -> Message:
        msg = Message(
            id=MessageId.generate(),
            proyecto_id=proyecto_id,
            task_id=task_id,
            sender_id=sender_id,
            contenido=contenido,
            fecha_envio=datetime.now(),
            tipo=tipo,
        )
        msg._events.append(MessageSent(message_id=msg.id, sender_id=sender_id, tipo=tipo))
        return msg

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
