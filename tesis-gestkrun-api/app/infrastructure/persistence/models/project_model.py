from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import EstadoProyecto
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class ProjectModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoProyecto] = mapped_column(
        Enum(EstadoProyecto, name="estado_proyecto_enum", create_type=True),
        nullable=False,
        server_default="ACTIVO",
    )
    fecha_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    wip_limit: Mapped[int] = mapped_column(Integer, nullable=False, server_default="3")
    owner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
