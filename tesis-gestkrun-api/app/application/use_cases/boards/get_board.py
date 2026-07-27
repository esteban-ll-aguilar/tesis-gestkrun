from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.entities.task import Task
from app.domain.enums import EstadoTarea
from app.domain.repositories.i_task_repository import ITaskRepository
from app.domain.value_objects import SprintId, TaskId, UserId


@dataclass
class BoardColumn:
    estado: str
    items: list[dict] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.items)


@dataclass
class BoardResult:
    sprint_id: str
    columns: dict[str, BoardColumn] = field(default_factory=dict)


class GetBoardUseCase:
    def __init__(self, task_repo: ITaskRepository):
        self._task_repo = task_repo

    async def execute(self, sprint_id: SprintId) -> BoardResult:
        tasks = await self._task_repo.list_by_sprint(sprint_id)
        columns = {estado.value: BoardColumn(estado=estado.value) for estado in EstadoTarea}
        for task in tasks:
            col = columns[task.estado.value]
            col.items.append({
                "id": str(task.id),
                "titulo": task.titulo,
                "descripcion": task.descripcion,
                "estado": task.estado.value,
                "assigned_to": str(task.assigned_to) if task.assigned_to else None,
            })
        return BoardResult(sprint_id=str(sprint_id), columns=columns)


class TransitionTaskUseCase:
    def __init__(self, task_repo: ITaskRepository):
        self._task_repo = task_repo

    async def execute(
        self, task_id: TaskId, to_estado: EstadoTarea, user_id: UserId
    ) -> Task:
        task = await self._task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        task.move_to(to_estado, user_id)
        await self._task_repo.save(task)
        return task
