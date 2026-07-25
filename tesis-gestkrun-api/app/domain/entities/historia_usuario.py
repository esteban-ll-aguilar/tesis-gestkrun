from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import Prioridad
from app.domain.events import DomainEvent
from app.domain.value_objects import (
    EpicaId,
    EstimacionEsfuerzo,
    HistoriaUsuarioId,
    ModuleId,
)


@dataclass
class HistoriaUsuario:
    id: HistoriaUsuarioId
    epica_id: EpicaId
    modulo_id: ModuleId | None
    titulo: str
    descripcion: str
    criterios_aceptacion: str
    prioridad: Prioridad
    estimacion: EstimacionEsfuerzo
    orden: int
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        epica_id: EpicaId,
        titulo: str,
        descripcion: str,
        criterios_aceptacion: str,
        prioridad: Prioridad,
        estimacion: EstimacionEsfuerzo,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> HistoriaUsuario:
        return HistoriaUsuario(
            id=HistoriaUsuarioId.generate(),
            epica_id=epica_id,
            modulo_id=modulo_id,
            titulo=titulo,
            descripcion=descripcion,
            criterios_aceptacion=criterios_aceptacion,
            prioridad=prioridad,
            estimacion=estimacion,
            orden=orden,
        )

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
