from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.infrastructure.persistence.models.base import Base, SoftDeleteMixin


class ModuleDeveloperModel(Base, SoftDeleteMixin):
    __tablename__ = "module_developers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    module_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("modules.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
