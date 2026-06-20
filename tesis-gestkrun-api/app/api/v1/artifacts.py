from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.domain.entities import Artifact, ArtifactVersion, User
from app.domain.enums import TipoArtefacto
from app.domain.value_objects import ArtifactId, ArtifactVersionId, TaskId
from app.infrastructure.persistence.repositories import (
    ArtifactRepository,
    ArtifactVersionRepository,
)

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("")
async def upload_artifact(
    task_id: str = Form(...),
    nombre: str = Form(...),
    tipo: str = Form("DOCUMENTO"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ArtifactRepository(db)
    version_repo = ArtifactVersionRepository(db)

    await file.read()
    content_url = f"/uploads/{task_id}/{nombre}"

    artifact = Artifact.create(
        task_id=TaskId(value=UUID(task_id)),
        nombre=nombre,
        tipo=TipoArtefacto(tipo),
    )
    await repo.save(artifact)

    version = ArtifactVersion(
        id=ArtifactVersionId.generate(),
        artifact_id=artifact.id,
        version=1,
        content_url=content_url,
        uploaded_by=current_user.id,
        created_at=datetime.now(),
    )
    await version_repo.save(version)

    return {
        "id": str(artifact.id),
        "nombre": artifact.nombre,
        "tipo": artifact.tipo.value,
        "version": version.version,
        "content_url": content_url,
    }


@router.get("/task/{task_id}")
async def list_artifacts(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ArtifactRepository(db)
    artifacts = await repo.list_by_task(TaskId(value=UUID(task_id)))
    return [
        {
            "id": str(a.id),
            "nombre": a.nombre,
            "tipo": a.tipo.value,
            "version_actual": a.version_actual,
        }
        for a in artifacts
    ]


@router.get("/{artifact_id}/versions")
async def list_versions(
    artifact_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ArtifactVersionRepository(db)
    versions = await repo.list_by_artifact(ArtifactId(value=UUID(artifact_id)))
    return [
        {
            "id": str(v.id),
            "version": v.version,
            "content_url": v.content_url,
            "uploaded_by": str(v.uploaded_by),
            "created_at": v.created_at.isoformat(),
        }
        for v in versions
    ]


@router.get("/{artifact_id}/download/{version}")
async def download_artifact(
    artifact_id: str,
    version: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ArtifactVersionRepository(db)
    versions = await repo.list_by_artifact(ArtifactId(value=UUID(artifact_id)))
    match = [v for v in versions if v.version == version]
    if not match:
        raise HTTPException(status_code=404, detail="Version not found")
    return {"content_url": match[0].content_url, "version": version}
