from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session, require_role
from app.application.backlog import (
    CreateEpicaUseCase,
    CreateHistoriaUsuarioUseCase,
    DeleteEpicaUseCase,
    DeleteHistoriaUsuarioUseCase,
    ListEpicasUseCase,
    ListHistoriasUseCase,
    PrioritizeBacklogUseCase,
    UpdateEpicaUseCase,
    UpdateHistoriaUsuarioUseCase,
)
from app.domain.entities import User
from app.domain.enums import Prioridad, Rol
from app.domain.value_objects import EpicaId, HistoriaUsuarioId, ProjectId
from app.infrastructure.persistence.repositories import (
    EpicaRepository,
    HistoriaUsuarioRepository,
    SprintRepository,
    TaskRepository,
)

router = APIRouter(prefix="/projects/{project_id}/backlog", tags=["backlog"])


class CreateEpicaRequest(BaseModel):
    titulo: str
    descripcion: str = ""
    prioridad: str = "MEDIA"
    modulo_id: str | None = None


class UpdateEpicaRequest(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    prioridad: str | None = None
    modulo_id: str | None = None


class CreateHistoriaRequest(BaseModel):
    epica_id: str
    titulo: str
    descripcion: str = ""
    criterios_aceptacion: str = ""
    prioridad: str = "MEDIA"
    estimacion: int = 1
    modulo_id: str | None = None


class UpdateHistoriaRequest(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    criterios_aceptacion: str | None = None
    prioridad: str | None = None
    estimacion: int | None = None
    modulo_id: str | None = None


class ReorderRequest(BaseModel):
    epica_ids: list[str] | None = None
    historia_ids: list[str] | None = None


@router.get("")
async def get_backlog(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = PrioritizeBacklogUseCase(
        EpicaRepository(db), HistoriaUsuarioRepository(db), TaskRepository(db), SprintRepository(db)
    )
    return await use_case.get_backlog(ProjectId(value=UUID(project_id)))


@router.post("/epicas")
async def create_epica(
    project_id: str,
    body: CreateEpicaRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = CreateEpicaUseCase(EpicaRepository(db))
    return await use_case.execute(
        ProjectId(value=UUID(project_id)),
        body.titulo, body.descripcion, Prioridad(body.prioridad),
        modulo_id=body.modulo_id,
    )


@router.get("/epicas")
async def list_epicas(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = ListEpicasUseCase(EpicaRepository(db))
    return await use_case.execute(ProjectId(value=UUID(project_id)))


@router.patch("/epicas/{epica_id}")
async def update_epica(
    project_id: str,
    epica_id: str,
    body: UpdateEpicaRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = UpdateEpicaUseCase(EpicaRepository(db))
    prioridad = Prioridad(body.prioridad) if body.prioridad else None
    result = await use_case.execute(
        EpicaId(value=UUID(epica_id)),
        titulo=body.titulo, descripcion=body.descripcion, prioridad=prioridad,
        modulo_id=body.modulo_id,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Epica not found")
    return result


@router.delete("/epicas/{epica_id}", status_code=204)
async def delete_epica(
    project_id: str,
    epica_id: str,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = DeleteEpicaUseCase(EpicaRepository(db))
    deleted = await use_case.execute(EpicaId(value=UUID(epica_id)))
    if not deleted:
        raise HTTPException(status_code=404, detail="Epica not found")


@router.get("/historias")
async def list_historias(
    project_id: str,
    epica_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    use_case = ListHistoriasUseCase(HistoriaUsuarioRepository(db))
    return await use_case.execute(EpicaId(value=UUID(epica_id)))


@router.post("/historias")
async def create_historia(
    project_id: str,
    body: CreateHistoriaRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    epica_repo = EpicaRepository(db)
    epica = await epica_repo.get_by_id(EpicaId(value=UUID(body.epica_id)))
    modulo_id = body.modulo_id or (str(epica.modulo_id) if epica and epica.modulo_id else None)
    use_case = CreateHistoriaUsuarioUseCase(HistoriaUsuarioRepository(db))
    return await use_case.execute(
        EpicaId(value=UUID(body.epica_id)), body.titulo, body.descripcion,
        body.criterios_aceptacion, Prioridad(body.prioridad),
        body.estimacion, modulo_id,
    )


@router.patch("/historias/{historia_id}")
async def update_historia(
    project_id: str,
    historia_id: str,
    body: UpdateHistoriaRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = UpdateHistoriaUsuarioUseCase(HistoriaUsuarioRepository(db))
    prioridad = Prioridad(body.prioridad) if body.prioridad else None
    result = await use_case.execute(
        HistoriaUsuarioId(value=UUID(historia_id)),
        titulo=body.titulo, descripcion=body.descripcion,
        criterios_aceptacion=body.criterios_aceptacion,
        prioridad=prioridad, estimacion=body.estimacion, modulo_id=body.modulo_id,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Historia not found")
    return result


@router.delete("/historias/{historia_id}", status_code=204)
async def delete_historia(
    project_id: str,
    historia_id: str,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = DeleteHistoriaUsuarioUseCase(HistoriaUsuarioRepository(db))
    deleted = await use_case.execute(HistoriaUsuarioId(value=UUID(historia_id)))
    if not deleted:
        raise HTTPException(status_code=404, detail="Historia not found")


@router.put("/prioritize")
async def prioritize_backlog(
    project_id: str,
    body: ReorderRequest,
    current_user: User = Depends(require_role(Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    use_case = PrioritizeBacklogUseCase(
        EpicaRepository(db), HistoriaUsuarioRepository(db)
    )
    if body.epica_ids is not None:
        await use_case.reorder_epicas(ProjectId(value=UUID(project_id)), body.epica_ids)
    if body.historia_ids is not None and body.epica_ids:
        await use_case.reorder_historias(
            EpicaId(value=UUID(body.epica_ids[0])), body.historia_ids
        )
    return {"status": "ok"}
