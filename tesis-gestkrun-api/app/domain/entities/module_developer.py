from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects import ModuleId, UserId


@dataclass
class ModuleDeveloper:
    id: str
    module_id: ModuleId
    user_id: UserId
    deleted_at: datetime | None = None
