from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import Prioridad
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class EpicaModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "epicas"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    prioridad: Mapped[Prioridad] = mapped_column(
        Enum(Prioridad, name="prioridad_enum", create_type=True),
        nullable=False,
        server_default="MEDIA",
    )
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default="ACTIVA")
    orden: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    modulo_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("modules.id"), nullable=True
    )
