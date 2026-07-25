from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.artifact_version import ArtifactVersion
from app.domain.value_objects import ArtifactId


class IArtifactVersionRepository(ABC):
    @abstractmethod
    async def save(self, version: ArtifactVersion) -> None: ...

    @abstractmethod
    async def list_by_artifact(self, artifact_id: ArtifactId) -> list[ArtifactVersion]: ...
