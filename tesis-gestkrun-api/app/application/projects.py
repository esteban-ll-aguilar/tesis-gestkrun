from dataclasses import dataclass
from datetime import UTC

from app.domain.entities import Project, ProjectAssignment
from app.domain.enums import Rol
from app.domain.repositories import (
    IProjectAssignmentRepository,
    IProjectRepository,
    IUserRepository,
)
from app.domain.value_objects import ProjectId, UserId


@dataclass
class CreateProjectDTO:
    nombre: str
    descripcion: str
    owner_id: UserId


@dataclass
class ProjectResult:
    id: str
    nombre: str
    descripcion: str
    estado: str
    owner_id: str


class CreateProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, dto: CreateProjectDTO) -> ProjectResult:
        project = Project.create(dto.nombre, dto.descripcion, dto.owner_id)
        await self._project_repo.save(project)
        return _project_to_result(project)


class GetProjectsUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self) -> list[ProjectResult]:
        projects = await self._project_repo.list_all()
        return [_project_to_result(p) for p in projects]


class GetProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, project_id: ProjectId) -> ProjectResult | None:
        project = await self._project_repo.get_by_id(project_id)
        return _project_to_result(project) if project else None


class UpdateProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(
        self, project_id: ProjectId, nombre: str | None = None,
        descripcion: str | None = None,
    ) -> ProjectResult | None:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return None
        project.update(nombre=nombre, descripcion=descripcion)
        await self._project_repo.save(project)
        return _project_to_result(project)


class DeleteProjectUseCase:
    def __init__(self, project_repo: IProjectRepository):
        self._project_repo = project_repo

    async def execute(self, project_id: ProjectId) -> bool:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            return False
        project.deleted_at = now()
        await self._project_repo.save(project)
        return True


class AssignTeamUseCase:
    def __init__(
        self, assignment_repo: IProjectAssignmentRepository,
        user_repo: IUserRepository,
    ):
        self._assignment_repo = assignment_repo
        self._user_repo = user_repo

    async def execute(
        self, project_id: ProjectId, user_id: UserId, rol: Rol,
    ) -> ProjectAssignment:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if rol not in (Rol.SCRUM_MASTER, Rol.DEVELOPER):
            raise ValueError("Invalid role for assignment")

        assignment = ProjectAssignment(
            id=str(ProjectId.generate()),
            project_id=project_id,
            user_id=user_id,
            rol=rol,
        )
        await self._assignment_repo.save(assignment)
        return assignment


def _project_to_result(project: Project) -> ProjectResult:
    return ProjectResult(
        id=str(project.id),
        nombre=project.nombre,
        descripcion=project.descripcion,
        estado=project.estado.value,
        owner_id=str(project.owner_id),
    )


def now():
    from datetime import datetime
    return datetime.now(UTC)
