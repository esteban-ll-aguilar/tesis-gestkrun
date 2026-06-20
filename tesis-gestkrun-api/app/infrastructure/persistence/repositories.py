from uuid import UUID

from sqlalchemy import func as sa_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import (
    Artifact,
    ArtifactVersion,
    Epica,
    HistoriaUsuario,
    Message,
    Module,
    Project,
    ProjectAssignment,
    Sprint,
    SprintEvento,
    Task,
    TaskStateTransition,
    User,
)
from app.domain.repositories import (
    IArtifactRepository,
    IArtifactVersionRepository,
    IEpicaRepository,
    IHistoriaUsuarioRepository,
    IMessageRepository,
    IModuleRepository,
    IProjectAssignmentRepository,
    IProjectRepository,
    ISprintEventoRepository,
    ISprintRepository,
    ITaskRepository,
    ITaskStateTransitionRepository,
    IUserRepository,
)
from app.domain.value_objects import (
    ArtifactId,
    ArtifactVersionId,
    Email,
    EpicaId,
    EstimacionEsfuerzo,
    HistoriaUsuarioId,
    MessageId,
    ModuleId,
    PasswordHash,
    ProjectId,
    SprintEventoId,
    SprintId,
    TaskId,
    UserId,
)
from app.infrastructure.persistence.models import (
    ArtifactModel,
    ArtifactVersionModel,
    EpicaModel,
    HistoriaUsuarioModel,
    MessageModel,
    ModuleModel,
    ProjectAssignmentModel,
    ProjectModel,
    SprintEventoModel,
    SprintModel,
    TaskModel,
    TaskStateTransitionModel,
    UserModel,
)


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        model = UserModel(
            id=str(user.id),
            nombre=user.nombre,
            email=str(user.email),
            password_hash=str(user.password_hash),
            rol=user.rol,
            fecha_registro=user.fecha_registro,
            deleted_at=user.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, user_id: UserId) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == str(user_id))
        )
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def list_all(self, include_deleted: bool = False) -> list[User]:
        query = select(UserModel)
        if not include_deleted:
            query = query.where(UserModel.deleted_at.is_(None))
        result = await self.session.execute(query)
        return [_user_from_model(m) for m in result.scalars()]

    async def delete(self, user_id: UserId) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == str(user_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class ProjectRepository(IProjectRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, project: Project) -> None:
        model = ProjectModel(
            id=str(project.id),
            nombre=project.nombre,
            descripcion=project.descripcion,
            estado=project.estado,
            fecha_inicio=project.fecha_inicio,
            owner_id=str(project.owner_id),
            deleted_at=project.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, project_id: ProjectId) -> Project | None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == str(project_id))
        )
        model = result.scalar_one_or_none()
        return _project_from_model(model) if model else None

    async def list_by_owner(self, owner_id: UserId) -> list[Project]:
        result = await self.session.execute(
            select(ProjectModel).where(
                ProjectModel.owner_id == str(owner_id),
                ProjectModel.deleted_at.is_(None),
            )
        )
        return [_project_from_model(m) for m in result.scalars()]

    async def list_all(self) -> list[Project]:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.deleted_at.is_(None))
        )
        return [_project_from_model(m) for m in result.scalars()]

    async def delete(self, project_id: ProjectId) -> None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == str(project_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class ProjectAssignmentRepository(IProjectAssignmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assignment: ProjectAssignment) -> None:
        model = ProjectAssignmentModel(
            id=str(assignment.id),
            project_id=str(assignment.project_id),
            user_id=str(assignment.user_id),
            rol=assignment.rol,
            deleted_at=assignment.deleted_at,
        )
        self.session.add(model)

    async def get_by_project_and_user(
        self, project_id: ProjectId, user_id: UserId,
    ) -> ProjectAssignment | None:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.user_id == str(user_id),
                ProjectAssignmentModel.deleted_at.is_(None),
            )
        )
        model = result.scalar_one_or_none()
        return _assignment_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[ProjectAssignment]:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.deleted_at.is_(None),
            )
        )
        return [_assignment_from_model(m) for m in result.scalars()]

    async def remove(self, project_id: ProjectId, user_id: UserId) -> None:
        result = await self.session.execute(
            select(ProjectAssignmentModel).where(
                ProjectAssignmentModel.project_id == str(project_id),
                ProjectAssignmentModel.user_id == str(user_id),
            )
        )
        model = result.scalar_one_or_none()
        if model:
            model.deleted_at = sa_func.now()


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


class EpicaRepository(IEpicaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, epica: Epica) -> None:
        model = EpicaModel(
            id=str(epica.id),
            project_id=str(epica.project_id),
            titulo=epica.titulo,
            descripcion=epica.descripcion,
            prioridad=epica.prioridad,
            estado=epica.estado,
            orden=epica.orden,
            deleted_at=epica.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, epica_id: EpicaId) -> Epica | None:
        result = await self.session.execute(
            select(EpicaModel).where(EpicaModel.id == str(epica_id))
        )
        model = result.scalar_one_or_none()
        return _epica_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[Epica]:
        result = await self.session.execute(
            select(EpicaModel).where(
                EpicaModel.project_id == str(project_id),
                EpicaModel.deleted_at.is_(None),
            ).order_by(EpicaModel.orden)
        )
        return [_epica_from_model(m) for m in result.scalars()]

    async def delete(self, epica_id: EpicaId) -> None:
        result = await self.session.execute(
            select(EpicaModel).where(EpicaModel.id == str(epica_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)

    async def get_max_orden(self, project_id: ProjectId) -> int:
        result = await self.session.execute(
            select(sa_func.max(EpicaModel.orden)).where(
                EpicaModel.project_id == str(project_id)
            )
        )
        return result.scalar() or 0


class HistoriaUsuarioRepository(IHistoriaUsuarioRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, historia: HistoriaUsuario) -> None:
        model = HistoriaUsuarioModel(
            id=str(historia.id),
            epica_id=str(historia.epica_id),
            modulo_id=str(historia.modulo_id) if historia.modulo_id else None,
            titulo=historia.titulo,
            descripcion=historia.descripcion,
            criterios_aceptacion=historia.criterios_aceptacion,
            prioridad=historia.prioridad,
            estimacion=int(historia.estimacion),
            orden=historia.orden,
            deleted_at=historia.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, historia_id: HistoriaUsuarioId) -> HistoriaUsuario | None:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(HistoriaUsuarioModel.id == str(historia_id))
        )
        model = result.scalar_one_or_none()
        return _historia_from_model(model) if model else None

    async def list_by_epica(self, epica_id: EpicaId) -> list[HistoriaUsuario]:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(
                HistoriaUsuarioModel.epica_id == str(epica_id),
                HistoriaUsuarioModel.deleted_at.is_(None),
            ).order_by(HistoriaUsuarioModel.orden)
        )
        return [_historia_from_model(m) for m in result.scalars()]

    async def list_by_project(self, project_id: ProjectId) -> list[HistoriaUsuario]:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).join(
                EpicaModel, HistoriaUsuarioModel.epica_id == EpicaModel.id
            ).where(
                EpicaModel.project_id == str(project_id),
                HistoriaUsuarioModel.deleted_at.is_(None),
            ).order_by(EpicaModel.orden, HistoriaUsuarioModel.orden)
        )
        return [_historia_from_model(m) for m in result.scalars()]

    async def delete(self, historia_id: HistoriaUsuarioId) -> None:
        result = await self.session.execute(
            select(HistoriaUsuarioModel).where(HistoriaUsuarioModel.id == str(historia_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class SprintRepository(ISprintRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, sprint: Sprint) -> None:
        model = SprintModel(
            id=str(sprint.id),
            project_id=str(sprint.project_id),
            nombre=sprint.nombre,
            objetivo=sprint.objetivo,
            duracion_dias=sprint.duracion_dias,
            fecha_inicio=sprint.fecha_inicio,
            fecha_fin=sprint.fecha_fin,
            estado=sprint.estado,
            deleted_at=sprint.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, sprint_id: SprintId) -> Sprint | None:
        result = await self.session.execute(
            select(SprintModel).where(SprintModel.id == str(sprint_id))
        )
        model = result.scalar_one_or_none()
        return _sprint_from_model(model) if model else None

    async def list_by_project(self, project_id: ProjectId) -> list[Sprint]:
        result = await self.session.execute(
            select(SprintModel).where(
                SprintModel.project_id == str(project_id),
                SprintModel.deleted_at.is_(None),
            ).order_by(SprintModel.fecha_inicio.desc())
        )
        return [_sprint_from_model(m) for m in result.scalars()]

    async def get_active_by_project(self, project_id: ProjectId) -> Sprint | None:
        from app.domain.enums import EstadoSprint
        result = await self.session.execute(
            select(SprintModel).where(
                SprintModel.project_id == str(project_id),
                SprintModel.estado == EstadoSprint.EN_EJECUCION,
                SprintModel.deleted_at.is_(None),
            )
        )
        model = result.scalar_one_or_none()
        return _sprint_from_model(model) if model else None

    async def delete(self, sprint_id: SprintId) -> None:
        result = await self.session.execute(
            select(SprintModel).where(SprintModel.id == str(sprint_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class SprintEventoRepository(ISprintEventoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, evento: SprintEvento) -> None:
        model = SprintEventoModel(
            id=str(evento.id),
            sprint_id=str(evento.sprint_id),
            tipo=evento.tipo,
            fecha=evento.fecha,
            notas=evento.notas,
            duracion_minutos=evento.duracion_minutos,
            created_by=str(evento.created_by),
        )
        self.session.add(model)

    async def list_by_sprint(self, sprint_id: SprintId) -> list[SprintEvento]:
        result = await self.session.execute(
            select(SprintEventoModel).where(
                SprintEventoModel.sprint_id == str(sprint_id)
            ).order_by(SprintEventoModel.fecha)
        )
        return [_sprint_evento_from_model(m) for m in result.scalars()]


class TaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, task: Task) -> None:
        model = TaskModel(
            id=str(task.id),
            historia_usuario_id=str(task.historia_usuario_id),
            sprint_id=str(task.sprint_id) if task.sprint_id else None,
            assigned_to=str(task.assigned_to) if task.assigned_to else None,
            titulo=task.titulo,
            descripcion=task.descripcion,
            estado=task.estado,
            fecha_creacion=task.fecha_creacion,
            fecha_limite=task.fecha_limite,
            deleted_at=task.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, task_id: TaskId) -> Task | None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one_or_none()
        return _task_from_model(model) if model else None

    async def list_by_sprint(self, sprint_id: SprintId) -> list[Task]:
        result = await self.session.execute(
            select(TaskModel).where(
                TaskModel.sprint_id == str(sprint_id),
                TaskModel.deleted_at.is_(None),
            )
        )
        return [_task_from_model(m) for m in result.scalars()]

    async def list_by_assigned_user(
        self, user_id: UserId, estado: str | None = None,
    ) -> list[Task]:
        query = select(TaskModel).where(
            TaskModel.assigned_to == str(user_id),
            TaskModel.deleted_at.is_(None),
        )
        if estado:
            query = query.where(TaskModel.estado == estado)
        result = await self.session.execute(query)
        return [_task_from_model(m) for m in result.scalars()]

    async def count_by_user_and_estado(self, user_id: UserId, estado: str) -> int:
        result = await self.session.execute(
            select(sa_func.count()).where(
                TaskModel.assigned_to == str(user_id),
                TaskModel.estado == estado,
                TaskModel.deleted_at.is_(None),
            )
        )
        return result.scalar() or 0

    async def delete(self, task_id: TaskId) -> None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class TaskStateTransitionRepository(ITaskStateTransitionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, transition: TaskStateTransition) -> None:
        model = TaskStateTransitionModel(
            id=str(transition.id),
            task_id=str(transition.task_id),
            from_estado=transition.from_estado,
            to_estado=transition.to_estado,
            timestamp=transition.timestamp,
            user_id=str(transition.user_id),
            reason=transition.reason,
        )
        self.session.add(model)

    async def list_by_task(self, task_id: TaskId) -> list[TaskStateTransition]:
        result = await self.session.execute(
            select(TaskStateTransitionModel).where(
                TaskStateTransitionModel.task_id == str(task_id)
            ).order_by(TaskStateTransitionModel.timestamp)
        )
        return [_transition_from_model(m) for m in result.scalars()]


class MessageRepository(IMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: Message) -> None:
        model = MessageModel(
            id=str(message.id),
            proyecto_id=str(message.proyecto_id) if message.proyecto_id else None,
            task_id=str(message.task_id) if message.task_id else None,
            sender_id=str(message.sender_id),
            contenido=message.contenido,
            fecha_envio=message.fecha_envio,
            tipo=message.tipo,
        )
        self.session.add(model)

    async def list_by_project(
        self, project_id: ProjectId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]:
        query = select(MessageModel).where(
            MessageModel.proyecto_id == str(project_id)
        ).order_by(MessageModel.fecha_envio.desc()).limit(limit)
        if cursor:
            query = query.where(MessageModel.id < cursor)
        result = await self.session.execute(query)
        return [_message_from_model(m) for m in result.scalars()]

    async def list_by_task(
        self, task_id: TaskId, cursor: str | None = None, limit: int = 50,
    ) -> list[Message]:
        query = select(MessageModel).where(
            MessageModel.task_id == str(task_id)
        ).order_by(MessageModel.fecha_envio.desc()).limit(limit)
        if cursor:
            query = query.where(MessageModel.id < cursor)
        result = await self.session.execute(query)
        return [_message_from_model(m) for m in result.scalars()]


class ArtifactRepository(IArtifactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, artifact: Artifact) -> None:
        model = ArtifactModel(
            id=str(artifact.id),
            task_id=str(artifact.task_id),
            nombre=artifact.nombre,
            tipo=artifact.tipo,
            version_actual=artifact.version_actual,
            deleted_at=artifact.deleted_at,
        )
        self.session.add(model)

    async def get_by_id(self, artifact_id: ArtifactId) -> Artifact | None:
        result = await self.session.execute(
            select(ArtifactModel).where(ArtifactModel.id == str(artifact_id))
        )
        model = result.scalar_one_or_none()
        return _artifact_from_model(model) if model else None

    async def list_by_task(self, task_id: TaskId) -> list[Artifact]:
        result = await self.session.execute(
            select(ArtifactModel).where(
                ArtifactModel.task_id == str(task_id),
                ArtifactModel.deleted_at.is_(None),
            )
        )
        return [_artifact_from_model(m) for m in result.scalars()]

    async def delete(self, artifact_id: ArtifactId) -> None:
        result = await self.session.execute(
            select(ArtifactModel).where(ArtifactModel.id == str(artifact_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)


class ArtifactVersionRepository(IArtifactVersionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, version: ArtifactVersion) -> None:
        model = ArtifactVersionModel(
            id=str(version.id),
            artifact_id=str(version.artifact_id),
            version=version.version,
            content_url=version.content_url,
            uploaded_by=str(version.uploaded_by),
            created_at=version.created_at,
        )
        self.session.add(model)

    async def list_by_artifact(self, artifact_id: ArtifactId) -> list[ArtifactVersion]:
        result = await self.session.execute(
            select(ArtifactVersionModel).where(
                ArtifactVersionModel.artifact_id == str(artifact_id)
            ).order_by(ArtifactVersionModel.version.desc())
        )
        return [_artifact_version_from_model(m) for m in result.scalars()]


def _user_from_model(model: UserModel) -> User:
    return User(
        id=UserId(value=UUID(model.id)),
        nombre=model.nombre,
        email=Email(model.email),
        password_hash=PasswordHash(model.password_hash),
        rol=model.rol,
        fecha_registro=model.fecha_registro,
        deleted_at=model.deleted_at,
    )


def _project_from_model(model: ProjectModel) -> Project:
    return Project(
        id=ProjectId(value=UUID(model.id)),
        nombre=model.nombre,
        descripcion=model.descripcion,
        estado=model.estado,
        fecha_inicio=model.fecha_inicio,
        owner_id=UserId(value=UUID(model.owner_id)),
        deleted_at=model.deleted_at,
    )


def _assignment_from_model(model: ProjectAssignmentModel) -> ProjectAssignment:
    return ProjectAssignment(
        id=model.id,
        project_id=ProjectId(value=UUID(model.project_id)),
        user_id=UserId(value=UUID(model.user_id)),
        rol=model.rol,
        deleted_at=model.deleted_at,
    )


def _module_from_model(model: ModuleModel) -> Module:
    return Module(
        id=ModuleId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        nombre=model.nombre,
        descripcion=model.descripcion,
        estado=model.estado,
        deleted_at=model.deleted_at,
    )


def _epica_from_model(model: EpicaModel) -> Epica:
    return Epica(
        id=EpicaId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        titulo=model.titulo,
        descripcion=model.descripcion,
        prioridad=model.prioridad,
        estado=model.estado,
        orden=model.orden,
        deleted_at=model.deleted_at,
    )


def _historia_from_model(model: HistoriaUsuarioModel) -> HistoriaUsuario:
    return HistoriaUsuario(
        id=HistoriaUsuarioId(value=UUID(model.id)),
        epica_id=EpicaId(value=UUID(model.epica_id)),
        modulo_id=ModuleId(value=UUID(model.modulo_id)) if model.modulo_id else None,
        titulo=model.titulo,
        descripcion=model.descripcion,
        criterios_aceptacion=model.criterios_aceptacion,
        prioridad=model.prioridad,
        estimacion=EstimacionEsfuerzo(model.estimacion),
        orden=model.orden,
        deleted_at=model.deleted_at,
    )


def _sprint_from_model(model: SprintModel) -> Sprint:
    return Sprint(
        id=SprintId(value=UUID(model.id)),
        project_id=ProjectId(value=UUID(model.project_id)),
        nombre=model.nombre,
        objetivo=model.objetivo,
        duracion_dias=model.duracion_dias,
        fecha_inicio=model.fecha_inicio,
        fecha_fin=model.fecha_fin,
        estado=model.estado,
        deleted_at=model.deleted_at,
    )


def _sprint_evento_from_model(model: SprintEventoModel) -> SprintEvento:
    return SprintEvento(
        id=SprintEventoId(value=UUID(model.id)),
        sprint_id=SprintId(value=UUID(model.sprint_id)),
        tipo=model.tipo,
        fecha=model.fecha,
        notas=model.notas,
        duracion_minutos=model.duracion_minutos,
        created_by=UserId(value=UUID(model.created_by)),
    )


def _task_from_model(model: TaskModel) -> Task:
    return Task(
        id=TaskId(value=UUID(model.id)),
        historia_usuario_id=HistoriaUsuarioId(value=UUID(model.historia_usuario_id)),
        sprint_id=SprintId(value=UUID(model.sprint_id)) if model.sprint_id else None,
        assigned_to=UserId(value=UUID(model.assigned_to)) if model.assigned_to else None,
        titulo=model.titulo,
        descripcion=model.descripcion,
        estado=model.estado,
        fecha_creacion=model.fecha_creacion,
        fecha_limite=model.fecha_limite,
        deleted_at=model.deleted_at,
    )


def _transition_from_model(model: TaskStateTransitionModel) -> TaskStateTransition:
    return TaskStateTransition(
        id=model.id,
        task_id=TaskId(value=UUID(model.task_id)),
        from_estado=model.from_estado,
        to_estado=model.to_estado,
        timestamp=model.timestamp,
        user_id=UserId(value=UUID(model.user_id)),
        reason=model.reason,
    )


def _message_from_model(model: MessageModel) -> Message:
    return Message(
        id=MessageId(value=UUID(model.id)),
        proyecto_id=ProjectId(value=UUID(model.proyecto_id)) if model.proyecto_id else None,
        task_id=TaskId(value=UUID(model.task_id)) if model.task_id else None,
        sender_id=UserId(value=UUID(model.sender_id)),
        contenido=model.contenido,
        fecha_envio=model.fecha_envio,
        tipo=model.tipo,
    )


def _artifact_from_model(model: ArtifactModel) -> Artifact:
    return Artifact(
        id=ArtifactId(value=UUID(model.id)),
        task_id=TaskId(value=UUID(model.task_id)),
        nombre=model.nombre,
        tipo=model.tipo,
        version_actual=model.version_actual,
        deleted_at=model.deleted_at,
    )


def _artifact_version_from_model(model: ArtifactVersionModel) -> ArtifactVersion:
    return ArtifactVersion(
        id=ArtifactVersionId(value=UUID(model.id)),
        artifact_id=ArtifactId(value=UUID(model.artifact_id)),
        version=model.version,
        content_url=model.content_url,
        uploaded_by=UserId(value=UUID(model.uploaded_by)),
        created_at=model.created_at,
    )
