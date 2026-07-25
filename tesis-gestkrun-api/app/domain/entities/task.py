from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from app.domain.enums import EstadoTarea
from app.domain.events import DomainEvent, TaskBlocked, TaskMoved
from app.domain.value_objects import HistoriaUsuarioId, SprintId, TaskId, UserId


@dataclass
class Task:
    id: TaskId
    historia_usuario_id: HistoriaUsuarioId
    sprint_id: SprintId | None
    assigned_to: UserId | None
    titulo: str
    descripcion: str
    estado: EstadoTarea
    fecha_creacion: datetime
    fecha_limite: date | None
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        historia_usuario_id: HistoriaUsuarioId,
        titulo: str,
        descripcion: str,
        sprint_id: SprintId | None = None,
        assigned_to: UserId | None = None,
        fecha_limite: date | None = None,
    ) -> Task:
        return Task(
            id=TaskId.generate(),
            historia_usuario_id=historia_usuario_id,
            sprint_id=sprint_id,
            assigned_to=assigned_to,
            titulo=titulo,
            descripcion=descripcion,
            estado=EstadoTarea.PENDIENTE,
            fecha_creacion=datetime.now(),
            fecha_limite=fecha_limite,
        )

    def assign_to(self, user_id: UserId) -> None:
        self.assigned_to = user_id

    def move_to(self, new_estado: EstadoTarea, user_id: UserId) -> None:
        old_estado = self.estado
        self.estado = new_estado
        self._events.append(TaskMoved(
            task_id=self.id, from_estado=old_estado, to_estado=new_estado, user_id=user_id
        ))

    def block(self, reason: str, blocked_by: UserId) -> None:
        self.estado = EstadoTarea.BLOQUEADO
        self._events.append(TaskBlocked(task_id=self.id, reason=reason, blocked_by=blocked_by))

    def unblock(self) -> None:
        if self.estado == EstadoTarea.BLOQUEADO:
            self.estado = EstadoTarea.EN_PROCESO

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
