from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.artifact import Artifact
from app.domain.value_objects import ArtifactId, TaskId


class IArtifactRepository(ABC):
    @abstractmethod
    async def save(self, artifact: Artifact) -> None: ...

    @abstractmethod
    async def get_by_id(self, artifact_id: ArtifactId) -> Artifact | None: ...

    @abstractmethod
    async def list_by_task(self, task_id: TaskId) -> list[Artifact]: ...

    @abstractmethod
    async def delete(self, artifact_id: ArtifactId) -> None: ...
