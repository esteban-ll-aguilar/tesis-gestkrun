from abc import ABC, abstractmethod

from app.domain.entities import (
    Artifact,
    ArtifactVersion,
    Epica,
    HistoriaUsuario,
    Message,
    Module,
    ModuleDeveloper,
    Project,
    ProjectAssignment,
    Sprint,
    SprintEvento,
    Task,
    TaskStateTransition,
    User,
)
from app.domain.value_objects import (
    ArtifactId,
    EpicaId,
    HistoriaUsuarioId,
    ModuleId,
    ProjectId,
    SprintId,
    TaskId,
    UserId,
)


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def list_all(self, include_deleted: bool = False) -> list[User]: ...

    @abstractmethod
    async def delete(self, user_id: UserId) -> None: ...


class IProjectRepository(ABC):
    @abstractmethod
    async def save(self, project: Project) -> None: ...

    @abstractmethod
    async def get_by_id(self, project_id: ProjectId) -> Project | None: ...

    @abstractmethod
    async def list_by_owner(self, owner_id: UserId) -> list[Project]: ...

    @abstractmethod
    async def list_all(self) -> list[Project]: ...

    @abstractmethod
    async def delete(self, project_id: ProjectId) -> None: ...


class IProjectAssignmentRepository(ABC):
    @abstractmethod
    async def save(self, assignment: ProjectAssignment) -> None: ...

    @abstractmethod
    async def get_by_project_and_user(
        self, project_id: ProjectId, user_id: UserId,
    ) -> ProjectAssignment | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[ProjectAssignment]: ...

    @abstractmethod
    async def remove(self, project_id: ProjectId, user_id: UserId) -> None: ...


class IModuleRepository(ABC):
    @abstractmethod
    async def save(self, module: Module) -> None: ...

    @abstractmethod
    async def get_by_id(self, module_id: ModuleId) -> Module | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Module]: ...

    @abstractmethod
    async def delete(self, module_id: ModuleId) -> None: ...


class IModuleDeveloperRepository(ABC):
    @abstractmethod
    async def save(self, assignment: ModuleDeveloper) -> None: ...

    @abstractmethod
    async def list_by_module(self, module_id: ModuleId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def list_by_user(self, user_id: UserId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[ModuleDeveloper]: ...

    @abstractmethod
    async def remove(self, module_id: ModuleId, user_id: UserId) -> None: ...


class IEpicaRepository(ABC):
    @abstractmethod
    async def save(self, epica: Epica) -> None: ...

    @abstractmethod
    async def get_by_id(self, epica_id: EpicaId) -> Epica | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Epica]: ...

    @abstractmethod
    async def delete(self, epica_id: EpicaId) -> None: ...

    @abstractmethod
    async def get_max_orden(self, project_id: ProjectId) -> int: ...


class IHistoriaUsuarioRepository(ABC):
    @abstractmethod
    async def save(self, historia: HistoriaUsuario) -> None: ...

    @abstractmethod
    async def get_by_id(self, historia_id: HistoriaUsuarioId) -> HistoriaUsuario | None: ...

    @abstractmethod
    async def list_by_epica(self, epica_id: EpicaId) -> list[HistoriaUsuario]: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[HistoriaUsuario]: ...

    @abstractmethod
    async def delete(self, historia_id: HistoriaUsuarioId) -> None: ...


class ISprintRepository(ABC):
    @abstractmethod
    async def save(self, sprint: Sprint) -> None: ...

    @abstractmethod
    async def get_by_id(self, sprint_id: SprintId) -> Sprint | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: ProjectId) -> list[Sprint]: ...

    @abstractmethod
    async def get_active_by_project(self, project_id: ProjectId) -> Sprint | None: ...

    @abstractmethod
    async def list_by_ids(self, sprint_ids: list[SprintId]) -> list[Sprint]: ...

    @abstractmethod
    async def delete(self, sprint_id: SprintId) -> None: ...


class ISprintEventoRepository(ABC):
    @abstractmethod
    async def save(self, evento: SprintEvento) -> None: ...

    @abstractmethod
    async def list_by_sprint(self, sprint_id: SprintId) -> list[SprintEvento]: ...


class ITaskRepository(ABC):
    @abstractmethod
    async def save(self, task: Task) -> None: ...

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Task | None: ...

    @abstractmethod
    async def list_by_sprint(self, sprint_id: SprintId) -> list[Task]: ...

    @abstractmethod
    async def list_by_sprints(self, sprint_ids: list[SprintId]) -> list[Task]: ...

    @abstractmethod
    async def list_by_assigned_user(
        self, user_id: UserId, estado: str | None = None,
    ) -> list[Task]: ...

    @abstractmethod
    async def count_by_user_and_estado(self, user_id: UserId, estado: str) -> int: ...

    @abstractmethod
    async def list_by_historia_ids(
        self, historia_ids: list[HistoriaUsuarioId],
    ) -> list[Task]: ...

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None: ...


class ITaskStateTransitionRepository(ABC):
    @abstractmethod
    async def save(self, transition: TaskStateTransition) -> None: ...

    @abstractmethod
    async def list_by_task(self, task_id: TaskId) -> list[TaskStateTransition]: ...


class IMessageRepository(ABC):
    @abstractmethod
    async def save(self, message: Message) -> None: ...

    @abstractmethod
    async def list_by_project(
        self, project_id: ProjectId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]: ...

    @abstractmethod
    async def list_by_task(
        self, task_id: TaskId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]: ...


class IArtifactRepository(ABC):
    @abstractmethod
    async def save(self, artifact: Artifact) -> None: ...

    @abstractmethod
    async def get_by_id(self, artifact_id: ArtifactId) -> Artifact | None: ...

    @abstractmethod
    async def list_by_task(self, task_id: TaskId) -> list[Artifact]: ...

    @abstractmethod
    async def delete(self, artifact_id: ArtifactId) -> None: ...


class IArtifactVersionRepository(ABC):
    @abstractmethod
    async def save(self, version: ArtifactVersion) -> None: ...

    @abstractmethod
    async def list_by_artifact(self, artifact_id: ArtifactId) -> list[ArtifactVersion]: ...
