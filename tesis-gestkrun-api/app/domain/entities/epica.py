from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import Prioridad
from app.domain.events import DomainEvent, EpicaCreated
from app.domain.value_objects import EpicaId, ModuleId, ProjectId


@dataclass
class Epica:
    id: EpicaId
    project_id: ProjectId
    titulo: str
    descripcion: str
    prioridad: Prioridad
    estado: str
    orden: int
    modulo_id: ModuleId | None = None
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        project_id: ProjectId, titulo: str, descripcion: str, prioridad: Prioridad, orden: int,
        modulo_id: ModuleId | None = None,
    ) -> Epica:
        epica = Epica(
            id=EpicaId.generate(),
            project_id=project_id,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado="ACTIVA",
            orden=orden,
            modulo_id=modulo_id,
        )
        epica._events.append(EpicaCreated(epica_id=epica.id, project_id=project_id, titulo=titulo))
        return epica

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
