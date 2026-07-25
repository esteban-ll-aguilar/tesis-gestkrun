from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import TipoEventoScrum
from app.infrastructure.persistence.models.base import Base


class SprintEventoModel(Base):
    __tablename__ = "sprint_eventos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    sprint_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sprints.id"), nullable=False
    )
    tipo: Mapped[TipoEventoScrum] = mapped_column(
        Enum(TipoEventoScrum, name="tipo_evento_scrum_enum", create_type=True),
        nullable=False,
    )
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notas: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    duracion_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
