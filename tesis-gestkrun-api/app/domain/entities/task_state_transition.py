from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import EstadoTarea
from app.domain.value_objects import TaskId, UserId


@dataclass
class TaskStateTransition:
    id: str
    task_id: TaskId
    from_estado: EstadoTarea
    to_estado: EstadoTarea
    timestamp: datetime
    user_id: UserId
    reason: str | None
