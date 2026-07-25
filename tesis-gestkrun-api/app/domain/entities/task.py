from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from app.domain.entities.task_state import TaskState, get_state
from app.domain.enums import EstadoTarea
from app.domain.events import DomainEvent, TaskBlocked, TaskMoved
from app.domain.value_objects import DomainError, HistoriaUsuarioId, SprintId, TaskId, UserId


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

    _state: TaskState = field(init=False, repr=False)
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self._state = get_state(self.estado)

    def _update_state(self, new_estado: EstadoTarea) -> None:
        self.estado = new_estado
        self._state = get_state(new_estado)

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

    def can_move_to(self, to_estado: EstadoTarea) -> bool:
        return self._state.can_transition_to(to_estado)

    def move_to(self, new_estado: EstadoTarea, user_id: UserId) -> None:
        if not self._state.can_transition_to(new_estado):
            raise DomainError(
                f"Cannot transition from {self.estado.value} to {new_estado.value}"
            )
        old_estado = self.estado
        self._update_state(new_estado)
        self._events.append(TaskMoved(
            task_id=self.id, from_estado=old_estado, to_estado=new_estado, user_id=user_id
        ))

    def block(self, reason: str, blocked_by: UserId) -> None:
        self._update_state(EstadoTarea.BLOQUEADO)
        self._events.append(TaskBlocked(task_id=self.id, reason=reason, blocked_by=blocked_by))

    def unblock(self) -> None:
        if self.estado == EstadoTarea.BLOQUEADO:
            self._update_state(EstadoTarea.EN_PROCESO)

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
