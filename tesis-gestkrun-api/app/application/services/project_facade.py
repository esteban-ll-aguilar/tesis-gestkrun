from __future__ import annotations

from datetime import date

from app.domain.entities.epica import Epica
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.entities.message import Message
from app.domain.entities.module import Module
from app.domain.entities.project import Project
from app.domain.entities.sprint import Sprint
from app.domain.entities.user import User
from app.domain.enums import Prioridad
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.repositories.i_message_repository import IMessageRepository
from app.domain.repositories.i_module_repository import IModuleRepository
from app.domain.repositories.i_project_assignment_repository import IProjectAssignmentRepository
from app.domain.repositories.i_project_repository import IProjectRepository
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.repositories.i_task_repository import ITaskRepository
from app.domain.repositories.i_user_repository import IUserRepository
from app.domain.value_objects import (
    EpicaId,
    EstimacionEsfuerzo,
    ModuleId,
    ProjectId,
    UserId,
)


class ProjectFacade:
    def __init__(
        self,
        project_repo: IProjectRepository,
        module_repo: IModuleRepository,
        sprint_repo: ISprintRepository,
        epica_repo: IEpicaRepository,
        historia_repo: IHistoriaUsuarioRepository,
        task_repo: ITaskRepository,
        message_repo: IMessageRepository,
        assignment_repo: IProjectAssignmentRepository,
        user_repo: IUserRepository,
    ):
        self._project_repo = project_repo
        self._module_repo = module_repo
        self._sprint_repo = sprint_repo
        self._epica_repo = epica_repo
        self._historia_repo = historia_repo
        self._task_repo = task_repo
        self._message_repo = message_repo
        self._assignment_repo = assignment_repo
        self._user_repo = user_repo

    async def create_project(
        self, nombre: str, descripcion: str, owner_id: UserId
    ) -> Project:
        project = Project.create(nombre, descripcion, owner_id)
        await self._project_repo.save(project)
        return project

    async def get_project(self, project_id: ProjectId) -> Project | None:
        return await self._project_repo.get_by_id(project_id)

    async def list_projects(self) -> list[Project]:
        return await self._project_repo.list_all()

    async def update_project(
        self, project_id: ProjectId, nombre: str | None = None, descripcion: str | None = None
    ) -> Project | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        project.update(nombre, descripcion)
        await self._project_repo.save(project)
        return project

    async def delete_project(self, project_id: ProjectId) -> None:
        await self._project_repo.delete(project_id)

    async def add_module(
        self, project_id: ProjectId, nombre: str, descripcion: str = ""
    ) -> Module | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        module = project.add_module(nombre, descripcion)
        await self._module_repo.save(module)
        return module

    async def list_modules(self, project_id: ProjectId) -> list[Module]:
        return await self._module_repo.list_by_project(project_id)

    async def plan_sprint(
        self,
        project_id: ProjectId,
        nombre: str,
        objetivo: str,
        duracion_dias: int,
        fecha_inicio: date,
        meeting_link: str = "",
    ) -> Sprint | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        sprint = project.plan_sprint(nombre, objetivo, duracion_dias, fecha_inicio, meeting_link)
        await self._sprint_repo.save(sprint)
        return sprint

    async def list_sprints(self, project_id: ProjectId) -> list[Sprint]:
        return await self._sprint_repo.list_by_project(project_id)

    async def create_epica(
        self,
        project_id: ProjectId,
        titulo: str,
        descripcion: str,
        prioridad: Prioridad,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> Epica | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        epica = project.create_epica(titulo, descripcion, prioridad, orden, modulo_id)
        await self._epica_repo.save(epica)
        return epica

    async def list_epicas(self, project_id: ProjectId) -> list[Epica]:
        return await self._epica_repo.list_by_project(project_id)

    async def create_historia(
        self,
        project_id: ProjectId,
        epica_id: EpicaId,
        titulo: str,
        descripcion: str,
        criterios_aceptacion: str,
        prioridad: Prioridad,
        estimacion: EstimacionEsfuerzo,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> HistoriaUsuario | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        hu = project.create_historia(
            epica_id, titulo, descripcion, criterios_aceptacion,
            prioridad, estimacion, orden, modulo_id,
        )
        await self._historia_repo.save(hu)
        return hu

    async def send_message(
        self,
        proyecto_id: ProjectId,
        contenido: str,
        sender_id: UserId,
        tipo: str = "PROYECTO",
    ) -> Message | None:
        project = await self._project_repo.get_by_id(proyecto_id)
        if not project:
            return None
        msg = project.add_message(contenido, sender_id, tipo)
        await self._message_repo.save(msg)
        return msg

    async def add_team_member(
        self, project_id: ProjectId, user_id: UserId
    ) -> None:
        from app.domain.entities.project_assignment import ProjectAssignment

        assignment = ProjectAssignment(project_id=project_id, user_id=user_id)
        await self._assignment_repo.save(assignment)

    async def get_team_members(self, project_id: ProjectId) -> list[User]:
        assignments = await self._assignment_repo.list_by_project(project_id)
        users = []
        for a in assignments:
            user = await self._user_repo.get_by_id(a.user_id)
            if user:
                users.append(user)
        return users
