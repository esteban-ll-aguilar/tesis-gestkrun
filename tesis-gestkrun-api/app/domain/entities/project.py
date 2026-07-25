from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from app.domain.enums import EstadoProyecto
from app.domain.events import DomainEvent, ProjectCreated
from app.domain.value_objects import ProjectId, UserId


@dataclass
class Project:
    id: ProjectId
    nombre: str
    descripcion: str
    estado: EstadoProyecto
    fecha_inicio: date
    owner_id: UserId
    wip_limit: int = 3
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(nombre: str, descripcion: str, owner_id: UserId, wip_limit: int = 3) -> Project:
        project = Project(
            id=ProjectId.generate(),
            nombre=nombre,
            descripcion=descripcion,
            estado=EstadoProyecto.ACTIVO,
            fecha_inicio=date.today(),
            owner_id=owner_id,
            wip_limit=wip_limit,
        )
        project._events.append(ProjectCreated(
            project_id=project.id, nombre=nombre, owner_id=owner_id
        ))
        return project

    def update(self, nombre: str | None = None, descripcion: str | None = None) -> None:
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion

    def change_status(self, new_estado: EstadoProyecto) -> None:
        self.estado = new_estado

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None
