from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent:
    event_id: str = ""
    occurred_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.occurred_at = self.occurred_at or datetime.now()


@dataclass
class UserRegistered(DomainEvent):
    user_id: Any = None
    email: Any = None
    rol: Any = None


@dataclass
class UserRoleChanged(DomainEvent):
    user_id: Any = None
    old_rol: Any = None
    new_rol: Any = None
    changed_by: Any = None


@dataclass
class UserDeactivated(DomainEvent):
    user_id: Any = None
    deactivated_by: Any = None


@dataclass
class ProjectCreated(DomainEvent):
    project_id: Any = None
    nombre: str = ""
    owner_id: Any = None


@dataclass
class ModuleAdded(DomainEvent):
    module_id: Any = None
    project_id: Any = None
    nombre: str = ""


@dataclass
class TeamAssigned(DomainEvent):
    project_id: Any = None
    user_id: Any = None
    rol: Any = None


@dataclass
class EpicaCreated(DomainEvent):
    epica_id: Any = None
    project_id: Any = None
    titulo: str = ""


@dataclass
class BacklogPrioritized(DomainEvent):
    project_id: Any = None
    reordered_by: Any = None


@dataclass
class SprintPlanned(DomainEvent):
    sprint_id: Any = None
    project_id: Any = None
    nombre: str = ""
    fecha_inicio: Any = None
    fecha_fin: Any = None


@dataclass
class SprintClosed(DomainEvent):
    sprint_id: Any = None
    project_id: Any = None
    closed_by: Any = None


@dataclass
class TaskMoved(DomainEvent):
    task_id: Any = None
    from_estado: Any = None
    to_estado: Any = None
    user_id: Any = None


@dataclass
class WIPViolated(DomainEvent):
    user_id: Any = None
    current_count: int = 0
    max_allowed: int = 0


@dataclass
class TaskBlocked(DomainEvent):
    task_id: Any = None
    reason: str = ""
    blocked_by: Any = None


@dataclass
class MessageSent(DomainEvent):
    message_id: Any = None
    sender_id: Any = None
    tipo: Any = None


@dataclass
class ArtifactUploaded(DomainEvent):
    artifact_id: Any = None
    task_id: Any = None
    nombre: str = ""
    tipo: Any = None
