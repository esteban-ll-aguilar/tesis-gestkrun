from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from app.domain.enums import EstadoSprint
from app.domain.events import DomainEvent, SprintClosed, SprintPlanned
from app.domain.value_objects import DomainError, ProjectId, SprintId, UserId


@dataclass
class Sprint:
    id: SprintId
    project_id: ProjectId
    nombre: str
    objetivo: str
    duracion_dias: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoSprint
    meeting_link: str = ""
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def plan(
        project_id: ProjectId,
        nombre: str,
        objetivo: str,
        duracion_dias: int,
        fecha_inicio: date,
        meeting_link: str = "",
    ) -> Sprint:
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        sprint = Sprint(
            id=SprintId.generate(),
            project_id=project_id,
            nombre=nombre,
            objetivo=objetivo,
            duracion_dias=duracion_dias,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=EstadoSprint.PLANIFICADO,
            meeting_link=meeting_link,
        )
        sprint._events.append(SprintPlanned(
            sprint_id=sprint.id, project_id=project_id, nombre=nombre,
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
        ))
        return sprint

    def start(self) -> None:
        if self.estado != EstadoSprint.PLANIFICADO:
            raise DomainError(f"Cannot start sprint in state {self.estado}")
        self.estado = EstadoSprint.EN_EJECUCION

    def close(self, closed_by: UserId) -> None:
        if self.estado != EstadoSprint.EN_EJECUCION:
            raise DomainError(f"Cannot close sprint in state {self.estado}")
        self.estado = EstadoSprint.FINALIZADO
        self._events.append(SprintClosed(
            sprint_id=self.id, project_id=self.project_id, closed_by=closed_by
        ))

    def cancel(self) -> None:
        self.estado = EstadoSprint.CANCELADO

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
