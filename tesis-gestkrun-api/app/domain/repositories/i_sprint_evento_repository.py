from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.sprint_evento import SprintEvento
from app.domain.value_objects import SprintId


class ISprintEventoRepository(ABC):
    @abstractmethod
    async def save(self, evento: SprintEvento) -> None: ...

    @abstractmethod
    async def list_by_sprint(self, sprint_id: SprintId) -> list[SprintEvento]: ...
