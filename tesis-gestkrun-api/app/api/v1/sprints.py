from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session, require_role
from app.application.use_cases.sprints.cancel_sprint import CancelSprintUseCase
from app.application.use_cases.sprints.close_sprint import CloseSprintUseCase
from app.application.use_cases.sprints.create_sprint_evento import CreateSprintEventoUseCase
from app.application.use_cases.sprints.get_sprint import GetSprintUseCase
from app.application.use_cases.sprints.list_sprint_eventos import ListSprintEventosUseCase
from app.application.use_cases.sprints.list_sprints import ListSprintsUseCase
from app.application.use_cases.sprints.plan_sprint import PlanSprintUseCase
from app.application.use_cases.sprints.start_sprint import StartSprintUseCase
from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.domain.enums import Rol, TipoEventoScrum
from app.domain.value_objects import HistoriaUsuarioId, ProjectId, SprintId
from app.infrastructure.persistence.repositories.historia_usuario_repository import (
    HistoriaUsuarioRepository,
)
from app.infrastructure.persistence.repositories.sprint_evento_repository import (
    SprintEventoRepository,
)
from app.infrastructure.persistence.repositories.sprint_repository import SprintRepository
from app.infrastructure.persistence.repositories.task_repository import TaskRepository

router = APIRouter(prefix="/projects/{project_id}/sprints", tags=["sprints"])


class PlanSprintRequest(BaseModel):
    nombre: str
    objetivo: str = ""
    duracion_dias: int = 14
    fecha_inicio: date
    historia_ids: list[str] = []
    meeting_link: str = ""


class CreateEventoRequest(BaseModel):
    tipo: str
    notas: str = ""
    duracion_minutos: int = 15


@router.post("")
async def plan_sprint(
    project_id: str,
    body: PlanSprintRequest,
    current_user: User = Depends(require_role(Rol.SCRUM_MASTER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = PlanSprintUseCase(SprintRepository(db))
    sprint = await use_case.execute(
        ProjectId(value=UUID(project_id)),
        body.nombre, body.objetivo, body.duracion_dias, body.fecha_inicio,
        meeting_link=body.meeting_link,
    )

    if body.historia_ids:
        historia_repo = HistoriaUsuarioRepository(db)
        task_repo = TaskRepository(db)
        sprint_uuid = sprint.id
        for hid in body.historia_ids:
            historia = await historia_repo.get_by_id(HistoriaUsuarioId(value=UUID(hid)))
            if historia:
                task = Task.create(
                    historia_usuario_id=historia.id,
                    titulo=historia.titulo,
                    descripcion=historia.descripcion,
                    sprint_id=SprintId(value=UUID(sprint_uuid)),
                )
                await task_repo.save(task)
        await db.commit()

    return sprint


@router.get("")
async def list_sprints(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = ListSprintsUseCase(SprintRepository(db))
    return await use_case.execute(ProjectId(value=UUID(project_id)))


@router.get("/{sprint_id}")
async def get_sprint(
    project_id: str,
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = GetSprintUseCase(SprintRepository(db))
    result = await use_case.execute(SprintId(value=UUID(sprint_id)))
    if not result:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return result


@router.post("/{sprint_id}/start")
async def start_sprint(
    project_id: str,
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = StartSprintUseCase(SprintRepository(db))
    try:
        return await use_case.execute(SprintId(value=UUID(sprint_id)))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{sprint_id}/close")
async def close_sprint(
    project_id: str,
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = CloseSprintUseCase(SprintRepository(db))
    try:
        return await use_case.execute(
            SprintId(value=UUID(sprint_id)), closed_by=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{sprint_id}/cancel")
async def cancel_sprint(
    project_id: str,
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = CancelSprintUseCase(SprintRepository(db))
    try:
        return await use_case.execute(SprintId(value=UUID(sprint_id)))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{sprint_id}/eventos")
async def create_evento(
    project_id: str,
    sprint_id: str,
    body: CreateEventoRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = CreateSprintEventoUseCase(SprintEventoRepository(db))
    return await use_case.execute(
        SprintId(value=UUID(sprint_id)),
        TipoEventoScrum(body.tipo), body.notas,
        body.duracion_minutos, current_user.id,
    )


@router.get("/{sprint_id}/eventos")
async def list_eventos(
    project_id: str,
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = ListSprintEventosUseCase(SprintEventoRepository(db))
    return await use_case.execute(SprintId(value=UUID(sprint_id)))
