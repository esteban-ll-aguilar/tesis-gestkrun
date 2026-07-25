from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import Rol
from app.domain.value_objects import ProjectId, UserId


@dataclass
class ProjectAssignment:
    id: str  # UUID string
    project_id: ProjectId
    user_id: UserId
    rol: Rol
    deleted_at: datetime | None = None
