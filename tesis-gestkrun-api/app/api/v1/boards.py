from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities import TaskStateTransition, User
from app.domain.enums import EstadoTarea
from app.domain.services import KanbanFlowService, WIPValidationService
from app.domain.value_objects import SprintId, TaskId
from app.infrastructure.persistence.repositories import (
    TaskRepository,
    TaskStateTransitionRepository,
)

DEFAULT_WIP_LIMIT = 3

router = APIRouter(prefix="/boards", tags=["boards"])


class TransitionRequest(BaseModel):
    to_estado: str
    reason: str | None = None


class BlockRequest(BaseModel):
    reason: str


@router.get("/{sprint_id}")
async def get_board(
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    task_repo = TaskRepository(db)
    tasks = await task_repo.list_by_sprint(SprintId(value=UUID(sprint_id)))
    columns = {estado.value: [] for estado in EstadoTarea}
    for task in tasks:
        columns[task.estado.value].append({
            "id": str(task.id),
            "titulo": task.titulo,
            "descripcion": task.descripcion,
            "estado": task.estado.value,
            "assigned_to": str(task.assigned_to) if task.assigned_to else None,
            "fecha_limite": task.fecha_limite.isoformat() if task.fecha_limite else None,
            "fecha_creacion": task.fecha_creacion.isoformat(),
        })
    return {
        "sprint_id": sprint_id,
        "columns": {k: {"items": v, "count": len(v)} for k, v in columns.items()},
    }


@router.patch("/tasks/{task_id}/transition")
async def transition_task(
    task_id: str,
    body: TransitionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    task_repo = TaskRepository(db)
    transition_repo = TaskStateTransitionRepository(db)

    task = await task_repo.get_by_id(TaskId(value=UUID(task_id)))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    to_estado = EstadoTarea(body.to_estado)
    flow_service = KanbanFlowService()

    if not flow_service.can_transition(task, to_estado):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {task.estado.value} to {to_estado.value}",
        )

    if to_estado == EstadoTarea.EN_PROCESO and not task.assigned_to:
        raise HTTPException(
            status_code=400,
            detail="Task must be assigned before moving to EN_PROCESO",
        )

    if to_estado == EstadoTarea.EN_PROCESO:
        wip_service = WIPValidationService()
        current_in_progress = await task_repo.count_by_user_and_estado(
            task.assigned_to, EstadoTarea.EN_PROCESO.value
        )

        violation = wip_service.validate(task.assigned_to, current_in_progress, DEFAULT_WIP_LIMIT)
        if violation:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"WIP limit ({DEFAULT_WIP_LIMIT}) reached for user. "
                    f"Current: {current_in_progress}"
                ),
            )

    old_estado = task.estado
    task.move_to(to_estado, current_user.id)

    transition = TaskStateTransition(
        id=str(uuid4()),
        task_id=task.id,
        from_estado=old_estado,
        to_estado=to_estado,
        timestamp=datetime.now(),
        user_id=current_user.id,
        reason=body.reason,
    )

    await task_repo.save(task)
    await transition_repo.save(transition)

    return {
        "id": str(task.id),
        "estado": task.estado.value,
        "transition": {
            "from": old_estado.value,
            "to": to_estado.value,
            "timestamp": transition.timestamp.isoformat(),
        },
    }


@router.patch("/tasks/{task_id}/block")
async def block_task(
    task_id: str,
    body: BlockRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    task_repo = TaskRepository(db)
    transition_repo = TaskStateTransitionRepository(db)

    task = await task_repo.get_by_id(TaskId(value=UUID(task_id)))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_estado = task.estado
    task.block(body.reason, current_user.id)

    transition = TaskStateTransition(
        id=str(uuid4()),
        task_id=task.id,
        from_estado=old_estado,
        to_estado=EstadoTarea.BLOQUEADO,
        timestamp=datetime.now(),
        user_id=current_user.id,
        reason=body.reason,
    )

    await task_repo.save(task)
    await transition_repo.save(transition)

    return {
        "id": str(task.id),
        "estado": task.estado.value,
        "blocked": True,
    }


@router.patch("/tasks/{task_id}/unblock")
async def unblock_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    task_repo = TaskRepository(db)
    transition_repo = TaskStateTransitionRepository(db)

    task = await task_repo.get_by_id(TaskId(value=UUID(task_id)))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_estado = task.estado
    if old_estado != EstadoTarea.BLOQUEADO:
        raise HTTPException(status_code=400, detail="Task is not blocked")

    task.unblock()

    if task.estado != old_estado:
        transition = TaskStateTransition(
            id=str(uuid4()),
            task_id=task.id,
            from_estado=old_estado,
            to_estado=task.estado,
            timestamp=datetime.now(),
            user_id=current_user.id,
            reason="Unblocked",
        )
        await transition_repo.save(transition)

    await task_repo.save(task)

    return {
        "id": str(task.id),
        "estado": task.estado.value,
        "blocked": False,
    }
