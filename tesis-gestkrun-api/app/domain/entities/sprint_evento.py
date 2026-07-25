from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import TipoEventoScrum
from app.domain.value_objects import SprintEventoId, SprintId, UserId


@dataclass
class SprintEvento:
    id: SprintEventoId
    sprint_id: SprintId
    tipo: TipoEventoScrum
    fecha: datetime
    notas: str
    duracion_minutos: int
    created_by: UserId
