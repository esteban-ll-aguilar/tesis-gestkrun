from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import EstadoSprint
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class SprintModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "sprints"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    objetivo: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    duracion_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime] = mapped_column(Date, nullable=False)
    meeting_link: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoSprint] = mapped_column(
        Enum(EstadoSprint, name="estado_sprint_enum", create_type=True),
        nullable=False,
        server_default="PLANIFICADO",
    )
