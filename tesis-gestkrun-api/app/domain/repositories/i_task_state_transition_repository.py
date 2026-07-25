from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.task_state_transition import TaskStateTransition
from app.domain.value_objects import TaskId


class ITaskStateTransitionRepository(ABC):
    @abstractmethod
    async def save(self, transition: TaskStateTransition) -> None: ...

    @abstractmethod
    async def list_by_task(self, task_id: TaskId) -> list[TaskStateTransition]: ...
