from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities.user import User
from app.domain.enums import EstadoTarea
from app.domain.value_objects import ProjectId
from app.infrastructure.persistence.models.task_model import TaskModel as TaskModel_
from app.infrastructure.persistence.repositories.sprint_repository import SprintRepository

router = APIRouter(prefix="/dashboard/{project_id}", tags=["dashboard"])


@router.get("/metrics")
async def get_metrics(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    total = await db.scalar(
        select(func.count()).select_from(TaskModel_).where(
            TaskModel_.deleted_at.is_(None)
        )
    ) or 0

    in_progress = await db.scalar(
        select(func.count()).select_from(TaskModel_).where(
            TaskModel_.estado == EstadoTarea.EN_PROCESO.value,
            TaskModel_.deleted_at.is_(None),
        )
    ) or 0

    blocked = await db.scalar(
        select(func.count()).select_from(TaskModel_).where(
            TaskModel_.estado == EstadoTarea.BLOQUEADO.value,
            TaskModel_.deleted_at.is_(None),
        )
    ) or 0

    completed = await db.scalar(
        select(func.count()).select_from(TaskModel_).where(
            TaskModel_.estado == EstadoTarea.TERMINADO.value,
            TaskModel_.deleted_at.is_(None),
        )
    ) or 0

    return {
        "total_tasks": total,
        "in_progress": in_progress,
        "blocked": blocked,
        "completed": completed,
        "completion_percentage": round((completed / total * 100) if total > 0 else 0, 1),
    }


@router.get("/velocity")
async def get_velocity(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    sprint_repo = SprintRepository(db)
    sprints = await sprint_repo.list_by_project(ProjectId(value=UUID(project_id)))
    result = []
    for s in sprints:
        tasks = await db.execute(
            select(TaskModel_.estado, func.count()).where(
                TaskModel_.sprint_id == str(s.id),
                TaskModel_.deleted_at.is_(None),
            ).group_by(TaskModel_.estado)
        )
        counts = dict(tasks.all())
        total = sum(counts.values())
        completed = counts.get(EstadoTarea.TERMINADO.value, 0)
        result.append({
            "sprint_id": str(s.id),
            "sprint_nombre": s.nombre,
            "fecha_inicio": s.fecha_inicio.isoformat(),
            "fecha_fin": s.fecha_fin.isoformat(),
            "estado": s.estado.value,
            "total_tasks": total,
            "completed_tasks": completed,
            "velocity": completed,
        })
    return result


@router.get("/task-distribution")
async def get_task_distribution(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    tasks = await db.execute(
        select(TaskModel_.estado, func.count()).where(
            TaskModel_.deleted_at.is_(None),
        ).group_by(TaskModel_.estado)
    )
    counts = dict(tasks.all())
    return [
        {"estado": estado.value, "count": counts.get(estado.value, 0)}
        for estado in EstadoTarea
    ]
