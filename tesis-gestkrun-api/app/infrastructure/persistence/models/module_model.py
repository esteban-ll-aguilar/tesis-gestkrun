from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import EstadoModulo
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class ModuleModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "modules"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoModulo] = mapped_column(
        Enum(EstadoModulo, name="estado_modulo_enum", create_type=True),
        nullable=False,
        server_default="ACTIVO",
    )
