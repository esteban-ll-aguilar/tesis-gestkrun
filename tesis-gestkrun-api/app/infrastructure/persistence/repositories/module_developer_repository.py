from __future__ import annotations

from uuid import UUID

from sqlalchemy import func as sa_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.module_developer import ModuleDeveloper
from app.domain.repositories.i_module_developer_repository import IModuleDeveloperRepository
from app.domain.value_objects import ModuleId, ProjectId, UserId
from app.infrastructure.persistence.models.module_developer_model import ModuleDeveloperModel
from app.infrastructure.persistence.models.module_model import ModuleModel


class ModuleDeveloperRepository(IModuleDeveloperRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assig: ModuleDeveloper) -> None:
        model = ModuleDeveloperModel(
            id=assig.id,
            module_id=str(assig.module_id),
            user_id=str(assig.user_id),
            deleted_at=assig.deleted_at,
        )
        await self.session.merge(model)

    async def list_by_module(self, module_id: ModuleId) -> list[ModuleDeveloper]:
        result = await self.session.execute(
            select(ModuleDeveloperModel).where(
                ModuleDeveloperModel.module_id == str(module_id),
                ModuleDeveloperModel.deleted_at.is_(None),
            )
        )
        return [_module_dev_from_model(m) for m in result.scalars()]

    async def list_by_user(self, user_id: UserId) -> list[ModuleDeveloper]:
        result = await self.session.execute(
            select(ModuleDeveloperModel).where(
                ModuleDeveloperModel.user_id == str(user_id),
                ModuleDeveloperModel.deleted_at.is_(None),
            )
        )
        return [_module_dev_from_model(m) for m in result.scalars()]

    async def list_by_project(self, project_id: ProjectId) -> list[ModuleDeveloper]:
        result = await self.session.execute(
            select(ModuleDeveloperModel).join(
                ModuleModel, ModuleDeveloperModel.module_id == ModuleModel.id
            ).where(
                ModuleModel.project_id == str(project_id),
                ModuleDeveloperModel.deleted_at.is_(None),
                ModuleModel.deleted_at.is_(None),
            )
        )
        return [_module_dev_from_model(m) for m in result.scalars()]

    async def remove(self, module_id: ModuleId, user_id: UserId) -> None:
        result = await self.session.execute(
            select(ModuleDeveloperModel).where(
                ModuleDeveloperModel.module_id == str(module_id),
                ModuleDeveloperModel.user_id == str(user_id),
            )
        )
        model = result.scalar_one_or_none()
        if model:
            model.deleted_at = sa_func.now()


def _module_dev_from_model(model: ModuleDeveloperModel) -> ModuleDeveloper:
    return ModuleDeveloper(
        id=model.id,
        module_id=ModuleId(value=UUID(model.module_id)),
        user_id=UserId(value=UUID(model.user_id)),
        deleted_at=model.deleted_at,
    )
