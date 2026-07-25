from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.domain.enums import Rol
from app.infrastructure.persistence.models.base import AuditMixin, Base, SoftDeleteMixin


class ProjectAssignmentModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "project_assignments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    rol: Mapped[Rol] = mapped_column(
        Enum(Rol, name="rol_enum", create_type=False),
        nullable=False,
    )
