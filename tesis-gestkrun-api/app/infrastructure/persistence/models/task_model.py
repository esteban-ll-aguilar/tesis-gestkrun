from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import EstadoTarea
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class TaskModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    historia_usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("historias_usuario.id"), nullable=False
    )
    sprint_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("sprints.id"), nullable=True
    )
    assigned_to: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoTarea] = mapped_column(
        Enum(EstadoTarea, name="estado_tarea_enum", create_type=True),
        nullable=False,
        server_default="PENDIENTE",
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_limite: Mapped[datetime | None] = mapped_column(Date, nullable=True)
