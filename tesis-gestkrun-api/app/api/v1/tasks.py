from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities import User
from app.domain.value_objects import ProjectId, SprintId, UserId
from app.infrastructure.persistence.repositories import (
    SprintRepository,
    TaskRepository,
)

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.get("")
async def list_tasks(
    project_id: str,
    sprint_id: str | None = None,
    assigned_to: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    task_repo = TaskRepository(db)
    sprint_repo = SprintRepository(db)

    if sprint_id:
        tasks = await task_repo.list_by_sprint(SprintId(value=UUID(sprint_id)))
    elif assigned_to:
        tasks = await task_repo.list_by_assigned_user(UserId(value=UUID(assigned_to)))
    else:
        sprints = await sprint_repo.list_by_project(ProjectId(value=UUID(project_id)))
        tasks = await task_repo.list_by_sprints([s.id for s in sprints if s.deleted_at is None])

    return [
        {
            "id": str(t.id),
            "titulo": t.titulo,
            "descripcion": t.descripcion,
            "estado": t.estado.value,
            "assigned_to": str(t.assigned_to) if t.assigned_to else None,
            "fecha_creacion": t.fecha_creacion.isoformat(),
            "fecha_limite": t.fecha_limite.isoformat() if t.fecha_limite else None,
        }
        for t in tasks
    ]
