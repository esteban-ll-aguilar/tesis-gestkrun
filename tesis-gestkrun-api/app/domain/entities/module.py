from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import EstadoModulo
from app.domain.events import DomainEvent, ModuleAdded
from app.domain.value_objects import ModuleId, ProjectId


@dataclass
class Module:
    id: ModuleId
    project_id: ProjectId
    nombre: str
    descripcion: str
    estado: EstadoModulo
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(project_id: ProjectId, nombre: str, descripcion: str = "") -> Module:
        module = Module(
            id=ModuleId.generate(),
            project_id=project_id,
            nombre=nombre,
            descripcion=descripcion,
            estado=EstadoModulo.ACTIVO,
        )
        module._events.append(ModuleAdded(
            module_id=module.id, project_id=project_id, nombre=nombre
        ))
        return module

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
