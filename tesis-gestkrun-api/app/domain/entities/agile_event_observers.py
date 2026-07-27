from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.sprint import Sprint


class AgileEventObserver:
    def on_sprint_event(
        self, sprint: Sprint, event_type: str, metadata: dict | None = None
    ) -> None:
        ...


@dataclass
class SprintPlanningObserver(AgileEventObserver):
    _logs: list[str] = field(default_factory=list)

    def on_sprint_event(
        self, sprint: Sprint, event_type: str, metadata: dict | None = None
    ) -> None:
        if event_type == "SPRINT_PLANNING":
            entry = (
                f"[{datetime.now().isoformat()}] Sprint Planning for "
                f"Sprint '{sprint.nombre}' (ID: {sprint.id}) - "
                f"Goal: {sprint.objetivo}"
            )
            self._logs.append(entry)

    @property
    def logs(self) -> list[str]:
        return list(self._logs)


@dataclass
class DailyScrumObserver(AgileEventObserver):
    _logs: list[str] = field(default_factory=list)

    def on_sprint_event(
        self, sprint: Sprint, event_type: str, metadata: dict | None = None
    ) -> None:
        if event_type == "DAILY_SCRUM":
            participant_count = (metadata or {}).get("participant_count", 0)
            entry = (
                f"[{datetime.now().isoformat()}] Daily Scrum for "
                f"Sprint '{sprint.nombre}' - "
                f"{participant_count} participants"
            )
            self._logs.append(entry)

    @property
    def logs(self) -> list[str]:
        return list(self._logs)


@dataclass
class SprintReviewObserver(AgileEventObserver):
    _logs: list[str] = field(default_factory=list)

    def on_sprint_event(
        self, sprint: Sprint, event_type: str, metadata: dict | None = None
    ) -> None:
        if event_type == "SPRINT_REVIEW":
            completed_items = (metadata or {}).get("completed_items", 0)
            feedback = (metadata or {}).get("feedback", "")
            entry = (
                f"[{datetime.now().isoformat()}] Sprint Review for "
                f"Sprint '{sprint.nombre}' - "
                f"{completed_items} items completed. Feedback: {feedback}"
            )
            self._logs.append(entry)

    @property
    def logs(self) -> list[str]:
        return list(self._logs)


@dataclass
class SprintRetrospectiveObserver(AgileEventObserver):
    _logs: list[str] = field(default_factory=list)

    def on_sprint_event(
        self, sprint: Sprint, event_type: str, metadata: dict | None = None
    ) -> None:
        if event_type == "SPRINT_RETROSPECTIVE":
            action_items = (metadata or {}).get("action_items", 0)
            entry = (
                f"[{datetime.now().isoformat()}] Sprint Retrospective for "
                f"Sprint '{sprint.nombre}' - "
                f"{action_items} action items identified"
            )
            self._logs.append(entry)

    @property
    def logs(self) -> list[str]:
        return list(self._logs)
