from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import TipoArtefacto
from app.domain.events import ArtifactUploaded, DomainEvent
from app.domain.value_objects import ArtifactId, TaskId


@dataclass
class Artifact:
    id: ArtifactId
    task_id: TaskId
    nombre: str
    tipo: TipoArtefacto
    version_actual: int
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(task_id: TaskId, nombre: str, tipo: TipoArtefacto) -> Artifact:
        artifact = Artifact(
            id=ArtifactId.generate(),
            task_id=task_id,
            nombre=nombre,
            tipo=tipo,
            version_actual=1,
        )
        artifact._events.append(ArtifactUploaded(
            artifact_id=artifact.id, task_id=task_id, nombre=nombre, tipo=tipo
        ))
        return artifact

    def new_version(self) -> int:
        self.version_actual += 1
        return self.version_actual

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
