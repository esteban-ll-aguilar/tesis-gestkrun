from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task_state_transition import TaskStateTransition
from app.domain.repositories.i_task_state_transition_repository import (
    ITaskStateTransitionRepository,
)
from app.domain.value_objects import TaskId, UserId
from app.infrastructure.persistence.models.task_state_transition_model import (
    TaskStateTransitionModel,
)


class TaskStateTransitionRepository(ITaskStateTransitionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, transition: TaskStateTransition) -> None:
        model = TaskStateTransitionModel(
            id=str(transition.id),
            task_id=str(transition.task_id),
            from_estado=transition.from_estado,
            to_estado=transition.to_estado,
            timestamp=transition.timestamp,
            user_id=str(transition.user_id),
            reason=transition.reason,
        )
        self.session.add(model)

    async def list_by_task(self, task_id: TaskId) -> list[TaskStateTransition]:
        result = await self.session.execute(
            select(TaskStateTransitionModel).where(
                TaskStateTransitionModel.task_id == str(task_id)
            ).order_by(TaskStateTransitionModel.timestamp)
        )
        return [_transition_from_model(m) for m in result.scalars()]


def _transition_from_model(model: TaskStateTransitionModel) -> TaskStateTransition:
    return TaskStateTransition(
        id=model.id,
        task_id=TaskId(value=UUID(model.task_id)),
        from_estado=model.from_estado,
        to_estado=model.to_estado,
        timestamp=model.timestamp,
        user_id=UserId(value=UUID(model.user_id)),
        reason=model.reason,
    )
