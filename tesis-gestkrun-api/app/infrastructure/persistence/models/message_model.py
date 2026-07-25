from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import TipoMensaje
from app.infrastructure.persistence.models.base import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    proyecto_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=True
    )
    task_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=True
    )
    sender_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_envio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    tipo: Mapped[TipoMensaje] = mapped_column(
        Enum(TipoMensaje, name="tipo_mensaje_enum", create_type=True),
        nullable=False,
    )
