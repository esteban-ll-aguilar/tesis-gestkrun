from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects import ArtifactId, ArtifactVersionId, UserId


@dataclass
class ArtifactVersion:
    id: ArtifactVersionId
    artifact_id: ArtifactId
    version: int
    content_url: str
    uploaded_by: UserId
    created_at: datetime
