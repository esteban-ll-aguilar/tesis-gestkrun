from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.infrastructure.persistence.models.base import Base


class ArtifactVersionModel(Base):
    __tablename__ = "artifact_versions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("artifacts.id"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_url: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_by: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
