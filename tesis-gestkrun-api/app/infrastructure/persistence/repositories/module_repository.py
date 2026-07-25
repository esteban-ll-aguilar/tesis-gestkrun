from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.module import Module
from app.domain.repositories.i_module_repository import IModuleRepository
from app.domain.value_objects import ModuleId, ProjectId
from app.infrastructure.persistence.models.module_model import ModuleModel


class ModuleRepository(IModuleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, module: Module) -> None:
        model = ModuleModel(
            id=str(module.id),
            project_id=str(module.project_id),
            nombre=module.nombre,
            descripcion=module.descripcion,
            estado=module.estado,
            deleted_at=module.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, module_id: ModuleId) -> Module | None:
        result = await self.session.execute(
            select(ModuleModel).where(ModuleModel.id == str(module_id))
        )
        model = result.scalar_one_or_none()
        return _module_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[Module]:
        result = await self.session.execute(
            select(ModuleModel).where(
                ModuleModel.project_id == str(project_id),
                ModuleModel.deleted_at.is_(None),
            )
        )
        return [_module_from_model(m) for m in result.scalars()]

    async def delete(self, module_id: ModuleId) -> None:
        result = await self.session.execute(
            select(ModuleModel).where(ModuleModel.id == str(module_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


def _module_from_model(model: ModuleModel) -> Module:
    return Module(
        id=ModuleId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        nombre=model.nombre,
        descripcion=model.descripcion,
        estado=model.estado,
        deleted_at=model.deleted_at,
    )
