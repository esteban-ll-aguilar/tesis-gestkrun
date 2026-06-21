from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities import Module, ModuleDeveloper
from app.domain.entities import User as UserEntity
from app.domain.value_objects import ModuleId, ProjectId, UserId
from app.infrastructure.persistence.repositories import (
    ModuleDeveloperRepository,
    ModuleRepository,
)

router = APIRouter(prefix="/projects/{project_id}/modules", tags=["modules"])


class CreateModuleRequest(BaseModel):
    nombre: str
    descripcion: str = ""


class UpdateModuleRequest(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


class AssignDeveloperRequest(BaseModel):
    user_id: str


@router.post("")
async def create_module(
    project_id: str,
    body: CreateModuleRequest,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleRepository(db)
    module = Module.create(ProjectId(value=UUID(project_id)), body.nombre, body.descripcion)
    await repo.save(module)
    return {
        "id": str(module.id), "nombre": module.nombre,
        "descripcion": module.descripcion, "estado": module.estado.value,
    }


@router.get("")
async def list_modules(
    project_id: str,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleRepository(db)
    modules = await repo.list_by_project(ProjectId(value=UUID(project_id)))
    return [
        {"id": str(m.id), "nombre": m.nombre, "estado": m.estado.value}
        for m in modules
    ]


@router.patch("/{module_id}")
async def update_module(
    project_id: str,
    module_id: str,
    body: UpdateModuleRequest,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleRepository(db)
    module = await repo.get_by_id(ModuleId(value=UUID(module_id)))
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    if body.nombre is not None:
        module.nombre = body.nombre
    if body.descripcion is not None:
        module.descripcion = body.descripcion
    await repo.save(module)
    return {
        "id": str(module.id), "nombre": module.nombre, "estado": module.estado.value,
    }


@router.delete("/{module_id}", status_code=204)
async def delete_module(
    project_id: str,
    module_id: str,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleRepository(db)
    module = await repo.get_by_id(ModuleId(value=UUID(module_id)))
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    await repo.delete(module.id)


@router.post("/{module_id}/developers")
async def assign_developer_to_module(
    project_id: str,
    module_id: str,
    body: AssignDeveloperRequest,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleDeveloperRepository(db)
    assig = ModuleDeveloper(
        id=str(uuid4()),
        module_id=ModuleId(value=UUID(module_id)),
        user_id=UserId(value=UUID(body.user_id)),
    )
    await repo.save(assig)
    return {"id": assig.id, "module_id": module_id, "user_id": body.user_id}


@router.get("/{module_id}/developers")
async def list_module_developers(
    project_id: str,
    module_id: str,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleDeveloperRepository(db)
    devs = await repo.list_by_module(ModuleId(value=UUID(module_id)))
    return [{"id": d.id, "module_id": str(d.module_id), "user_id": str(d.user_id)} for d in devs]


@router.delete("/{module_id}/developers/{user_id}", status_code=204)
async def remove_developer_from_module(
    project_id: str,
    module_id: str,
    user_id: str,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ModuleDeveloperRepository(db)
    await repo.remove(ModuleId(value=UUID(module_id)), UserId(value=UUID(user_id)))
