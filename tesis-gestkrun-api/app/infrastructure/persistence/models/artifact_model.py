from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import TipoArtefacto
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class ArtifactModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoArtefacto] = mapped_column(
        Enum(TipoArtefacto, name="tipo_artefacto_enum", create_type=True),
        nullable=False,
    )
    version_actual: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )
