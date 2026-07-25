from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.artifact import Artifact
from app.domain.repositories.i_artifact_repository import IArtifactRepository
from app.domain.value_objects import ArtifactId, TaskId
from app.infrastructure.persistence.models.artifact_model import ArtifactModel


class ArtifactRepository(IArtifactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, artifact: Artifact) -> None:
        model = ArtifactModel(
            id=str(artifact.id),
            task_id=str(artifact.task_id),
            nombre=artifact.nombre,
            tipo=artifact.tipo,
            version_actual=artifact.version_actual,
            deleted_at=artifact.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, artifact_id: ArtifactId) -> Artifact | None:
        result = await self.session.execute(
            select(ArtifactModel).where(ArtifactModel.id == str(artifact_id))
        )
        model = result.scalar_one_or_none()
        return _artifact_from_model(model) if model else None

    async def list_by_task(self, task_id: TaskId) -> list[Artifact]:
        result = await self.session.execute(
            select(ArtifactModel).where(
                ArtifactModel.task_id == str(task_id),
                ArtifactModel.deleted_at.is_(None),
            )
        )
        return [_artifact_from_model(m) for m in result.scalars()]

    async def delete(self, artifact_id: ArtifactId) -> None:
        result = await self.session.execute(
            select(ArtifactModel).where(ArtifactModel.id == str(artifact_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _artifact_from_model(model: ArtifactModel) -> Artifact:
    return Artifact(
        id=ArtifactId(value=UUID(model.id)),
        task_id=TaskId(value=UUID(model.task_id)),
        nombre=model.nombre,
        tipo=model.tipo,
        version_actual=model.version_actual,
        deleted_at=model.deleted_at,
    )
