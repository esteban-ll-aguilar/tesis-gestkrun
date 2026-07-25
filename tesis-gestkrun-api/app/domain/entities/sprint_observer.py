from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.sprint import Sprint


class SprintObserver(ABC):
    @abstractmethod
    def on_sprint_started(self, sprint: Sprint) -> None:
        ...

    @abstractmethod
    def on_sprint_closed(self, sprint: Sprint) -> None:
        ...

    @abstractmethod
    def on_sprint_cancelled(self, sprint: Sprint) -> None:
        ...


@dataclass
class AuditLogObserver(SprintObserver):
    _log: list[str] = field(default_factory=list)

    def on_sprint_started(self, sprint: Sprint) -> None:
        self._log.append(f"Sprint {sprint.id} started at {sprint.fecha_inicio}")

    def on_sprint_closed(self, sprint: Sprint) -> None:
        self._log.append(f"Sprint {sprint.id} closed")

    def on_sprint_cancelled(self, sprint: Sprint) -> None:
        self._log.append(f"Sprint {sprint.id} cancelled")


@dataclass
class MetricsObserver(SprintObserver):
    _metrics: dict[str, int] = field(
        default_factory=lambda: {"started": 0, "closed": 0, "cancelled": 0}
    )

    def on_sprint_started(self, sprint: Sprint) -> None:
        self._metrics["started"] += 1

    def on_sprint_closed(self, sprint: Sprint) -> None:
        self._metrics["closed"] += 1

    def on_sprint_cancelled(self, sprint: Sprint) -> None:
        self._metrics["cancelled"] += 1

    def summary(self) -> dict[str, int]:
        return dict(self._metrics)
