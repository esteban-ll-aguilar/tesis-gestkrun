from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.artifact_version import ArtifactVersion
from app.domain.repositories.i_artifact_version_repository import IArtifactVersionRepository
from app.domain.value_objects import ArtifactId, ArtifactVersionId, UserId
from app.infrastructure.persistence.models.artifact_version_model import ArtifactVersionModel


class ArtifactVersionRepository(IArtifactVersionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, version: ArtifactVersion) -> None:
        model = ArtifactVersionModel(
            id=str(version.id),
            artifact_id=str(version.artifact_id),
            version=version.version,
            content_url=version.content_url,
            uploaded_by=str(version.uploaded_by),
            created_at=version.created_at,
        )
        self.session.add(model)

    async def list_by_artifact(self, artifact_id: ArtifactId) -> list[ArtifactVersion]:
        result = await self.session.execute(
            select(ArtifactVersionModel).where(
                ArtifactVersionModel.artifact_id == str(artifact_id)
            ).order_by(ArtifactVersionModel.version.desc())
        )
        return [_artifact_version_from_model(m) for m in result.scalars()]


def _artifact_version_from_model(model: ArtifactVersionModel) -> ArtifactVersion:
    return ArtifactVersion(
        id=ArtifactVersionId(value=UUID(model.id)),
        artifact_id=ArtifactId(value=UUID(model.artifact_id)),
        version=model.version,
        content_url=model.content_url,
        uploaded_by=UserId(value=UUID(model.uploaded_by)),
        created_at=model.created_at,
    )
