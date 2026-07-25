from __future__ import annotations

from uuid import UUID

from sqlalchemy import func as sa_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.domain.repositories.i_task_repository import ITaskRepository
from app.domain.value_objects import (
    HistoriaUsuarioId,
    SprintId,
    TaskId,
    UserId,
)
from app.infrastructure.persistence.models.task_model import TaskModel


class TaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, task: Task) -> None:
        model = TaskModel(
            id=str(task.id),
            historia_usuario_id=str(task.historia_usuario_id),
            sprint_id=str(task.sprint_id) if task.sprint_id else None,
            assigned_to=str(task.assigned_to) if task.assigned_to else None,
            titulo=task.titulo,
            descripcion=task.descripcion,
            estado=task.estado,
            fecha_creacion=task.fecha_creacion,
            fecha_limite=task.fecha_limite,
            deleted_at=task.deleted_at,
        )
        await self.session.merge(model)

    async def get_by_id(self, task_id: TaskId) -> Task | None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one_or_none()
        return _task_from_model(model) if model else None

    async def list_by_sprint(self, sprint_id: SprintId) -> list[Task]:
        result = await self.session.execute(
            select(TaskModel).where(
                TaskModel.sprint_id == str(sprint_id),
                TaskModel.deleted_at.is_(None),
            )
        )
        return [_task_from_model(m) for m in result.scalars()]

    async def list_by_sprints(self, sprint_ids: list[SprintId]) -> list[Task]:
        str_ids = [str(s) for s in sprint_ids]
        result = await self.session.execute(
            select(TaskModel).where(
                TaskModel.sprint_id.in_(str_ids),
                TaskModel.deleted_at.is_(None),
            )
        )
        return [_task_from_model(m) for m in result.scalars()]

    async def list_by_assigned_user(
        self, user_id: UserId, estado: str | None = None,
    ) -> list[Task]:
        query = select(TaskModel).where(
            TaskModel.assigned_to == str(user_id),
            TaskModel.deleted_at.is_(None),
        )
        if estado:
            query = query.where(TaskModel.estado == estado)
        result = await self.session.execute(query)
        return [_task_from_model(m) for m in result.scalars()]

    async def list_by_historia_ids(
        self, historia_ids: list[HistoriaUsuarioId],
    ) -> list[Task]:
        str_ids = [str(h) for h in historia_ids]
        result = await self.session.execute(
            select(TaskModel).where(
                TaskModel.historia_usuario_id.in_(str_ids),
                TaskModel.deleted_at.is_(None),
            )
        )
        return [_task_from_model(m) for m in result.scalars()]

    async def count_by_user_and_estado(self, user_id: UserId, estado: str) -> int:
        result = await self.session.execute(
            select(sa_func.count()).where(
                TaskModel.assigned_to == str(user_id),
                TaskModel.estado == estado,
                TaskModel.deleted_at.is_(None),
            )
        )
        return result.scalar() or 0

    async def delete(self, task_id: TaskId) -> None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _task_from_model(model: TaskModel) -> Task:
    return Task(
        id=TaskId(value=UUID(model.id)),
        historia_usuario_id=HistoriaUsuarioId(value=UUID(model.historia_usuario_id)),
        sprint_id=SprintId(value=UUID(model.sprint_id)) if model.sprint_id else None,
        assigned_to=UserId(value=UUID(model.assigned_to)) if model.assigned_to else None,
        titulo=model.titulo,
        descripcion=model.descripcion,
        estado=model.estado,
        fecha_creacion=model.fecha_creacion,
        fecha_limite=model.fecha_limite,
        deleted_at=model.deleted_at,
    )
