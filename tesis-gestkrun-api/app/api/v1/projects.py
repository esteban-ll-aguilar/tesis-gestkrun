from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session, require_role
from app.application.dto.projects import CreateProjectDTO
from app.application.use_cases.projects.assign_team import AssignTeamUseCase
from app.application.use_cases.projects.create_project import CreateProjectUseCase
from app.application.use_cases.projects.delete_project import DeleteProjectUseCase
from app.application.use_cases.projects.get_project import GetProjectUseCase
from app.application.use_cases.projects.get_projects import GetProjectsUseCase
from app.application.use_cases.projects.update_project import UpdateProjectUseCase
from app.domain.entities.user import User
from app.domain.enums import Rol
from app.domain.value_objects import ProjectId, UserId
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.repositories.project_assignment_repository import (
    ProjectAssignmentRepository,
)
from app.infrastructure.persistence.repositories.project_repository import ProjectRepository
from app.infrastructure.persistence.repositories.user_repository import UserRepository

router = APIRouter(prefix="/projects", tags=["projects"])


class CreateProjectRequest(BaseModel):
    nombre: str
    descripcion: str = ""


class UpdateProjectRequest(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


class AssignTeamRequest(BaseModel):
    user_id: str
    rol: str


@router.post("")
async def create_project(
    body: CreateProjectRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = CreateProjectUseCase(ProjectRepository(db))
    result = await use_case.execute(CreateProjectDTO(
        nombre=body.nombre, descripcion=body.descripcion,
        owner_id=current_user.id,
    ))
    return result


@router.get("")
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = GetProjectsUseCase(ProjectRepository(db))
    return await use_case.execute()


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = GetProjectUseCase(ProjectRepository(db))
    result = await use_case.execute(ProjectId(value=UUID(project_id)))
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@router.patch("/{project_id}")
async def update_project(
    project_id: str,
    body: UpdateProjectRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = UpdateProjectUseCase(ProjectRepository(db))
    result = await use_case.execute(
        ProjectId(value=UUID(project_id)),
        nombre=body.nombre, descripcion=body.descripcion,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = DeleteProjectUseCase(ProjectRepository(db))
    deleted = await use_case.execute(ProjectId(value=UUID(project_id)))
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/{project_id}/assignments")
async def assign_team(
    project_id: str,
    body: AssignTeamRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = AssignTeamUseCase(
        ProjectAssignmentRepository(db), UserRepository(db)
    )
    try:
        result = await use_case.execute(
            ProjectId(value=UUID(project_id)),
            UserId(value=UUID(body.user_id)),
            Rol(body.rol),
        )
        return {"id": result.id, "project_id": project_id, "user_id": body.user_id, "rol": body.rol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{project_id}/assignments/{user_id}")
async def remove_assignment(
    project_id: str,
    user_id: str,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    repo = ProjectAssignmentRepository(db)
    await repo.remove(ProjectId(value=UUID(project_id)), UserId(value=UUID(user_id)))
    await db.commit()
    return {"message": "Assignment removed"}


@router.get("/{project_id}/assignments")
async def list_assignments(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ProjectAssignmentRepository(db)
    assignments = await repo.list_by_project(ProjectId(value=UUID(project_id)))

    result = []
    for a in assignments:
        user = await db.get(UserModel, str(a.user_id))
        result.append({
            "id": a.id,
            "user_id": str(a.user_id),
            "nombre": user.nombre if user else None,
            "email": user.email if user else None,
            "rol": a.rol.value,
        })
    return result
