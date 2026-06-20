from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from app.domain.enums import (
    EstadoModulo,
    EstadoProyecto,
    EstadoSprint,
    EstadoTarea,
    Prioridad,
    Rol,
    TipoArtefacto,
    TipoEventoScrum,
    TipoMensaje,
)
from app.domain.events import (
    ArtifactUploaded,
    DomainEvent,
    EpicaCreated,
    MessageSent,
    ModuleAdded,
    ProjectCreated,
    SprintClosed,
    SprintPlanned,
    TaskBlocked,
    TaskMoved,
    UserDeactivated,
    UserRegistered,
    UserRoleChanged,
)
from app.domain.value_objects import (
    ArtifactId,
    ArtifactVersionId,
    DomainError,
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


@dataclass
class User:
    id: UserId
    nombre: str
    email: Email
    password_hash: PasswordHash
    rol: Rol
    fecha_registro: datetime
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def register(nombre: str, email: Email, password_hash: PasswordHash) -> User:
        user = User(
            id=UserId.generate(),
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=Rol.DEVELOPER,
            fecha_registro=datetime.now(),
        )
        user._events.append(UserRegistered(user_id=user.id, email=email, rol=user.rol))
        return user

    def change_role(self, new_rol: Rol, changed_by: UserId) -> None:
        old_rol = self.rol
        self.rol = new_rol
        self._events.append(UserRoleChanged(
            user_id=self.id, old_rol=old_rol, new_rol=new_rol, changed_by=changed_by
        ))

    def deactivate(self, deactivated_by: UserId) -> None:
        self.deleted_at = datetime.now()
        self._events.append(UserDeactivated(user_id=self.id, deactivated_by=deactivated_by))

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None


@dataclass
class Project:
    id: ProjectId
    nombre: str
    descripcion: str
    estado: EstadoProyecto
    fecha_inicio: date
    owner_id: UserId
    wip_limit: int = 3
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(nombre: str, descripcion: str, owner_id: UserId, wip_limit: int = 3) -> Project:
        project = Project(
            id=ProjectId.generate(),
            nombre=nombre,
            descripcion=descripcion,
            estado=EstadoProyecto.ACTIVO,
            fecha_inicio=date.today(),
            owner_id=owner_id,
            wip_limit=wip_limit,
        )
        project._events.append(ProjectCreated(
            project_id=project.id, nombre=nombre, owner_id=owner_id
        ))
        return project

    def update(self, nombre: str | None = None, descripcion: str | None = None) -> None:
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion

    def change_status(self, new_estado: EstadoProyecto) -> None:
        self.estado = new_estado

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None


@dataclass
class ProjectAssignment:
    id: str  # UUID string
    project_id: ProjectId
    user_id: UserId
    rol: Rol
    deleted_at: datetime | None = None


@dataclass
class Module:
    id: ModuleId
    project_id: ProjectId
    nombre: str
    descripcion: str
    estado: EstadoModulo
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(project_id: ProjectId, nombre: str, descripcion: str = "") -> Module:
        module = Module(
            id=ModuleId.generate(),
            project_id=project_id,
            nombre=nombre,
            descripcion=descripcion,
            estado=EstadoModulo.ACTIVO,
        )
        module._events.append(ModuleAdded(
            module_id=module.id, project_id=project_id, nombre=nombre
        ))
        return module

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class Epica:
    id: EpicaId
    project_id: ProjectId
    titulo: str
    descripcion: str
    prioridad: Prioridad
    estado: str
    orden: int
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        project_id: ProjectId, titulo: str, descripcion: str, prioridad: Prioridad, orden: int,
    ) -> Epica:
        epica = Epica(
            id=EpicaId.generate(),
            project_id=project_id,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado="ACTIVA",
            orden=orden,
        )
        epica._events.append(EpicaCreated(epica_id=epica.id, project_id=project_id, titulo=titulo))
        return epica

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class HistoriaUsuario:
    id: HistoriaUsuarioId
    epica_id: EpicaId
    modulo_id: ModuleId | None
    titulo: str
    descripcion: str
    criterios_aceptacion: str
    prioridad: Prioridad
    estimacion: EstimacionEsfuerzo
    orden: int
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        epica_id: EpicaId,
        titulo: str,
        descripcion: str,
        criterios_aceptacion: str,
        prioridad: Prioridad,
        estimacion: EstimacionEsfuerzo,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> HistoriaUsuario:
        return HistoriaUsuario(
            id=HistoriaUsuarioId.generate(),
            epica_id=epica_id,
            modulo_id=modulo_id,
            titulo=titulo,
            descripcion=descripcion,
            criterios_aceptacion=criterios_aceptacion,
            prioridad=prioridad,
            estimacion=estimacion,
            orden=orden,
        )

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class Sprint:
    id: SprintId
    project_id: ProjectId
    nombre: str
    objetivo: str
    duracion_dias: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoSprint
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def plan(
        project_id: ProjectId,
        nombre: str,
        objetivo: str,
        duracion_dias: int,
        fecha_inicio: date,
    ) -> Sprint:
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        sprint = Sprint(
            id=SprintId.generate(),
            project_id=project_id,
            nombre=nombre,
            objetivo=objetivo,
            duracion_dias=duracion_dias,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=EstadoSprint.PLANIFICADO,
        )
        sprint._events.append(SprintPlanned(
            sprint_id=sprint.id, project_id=project_id, nombre=nombre,
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
        ))
        return sprint

    def start(self) -> None:
        if self.estado != EstadoSprint.PLANIFICADO:
            raise DomainError(f"Cannot start sprint in state {self.estado}")
        self.estado = EstadoSprint.EN_EJECUCION

    def close(self, closed_by: UserId) -> None:
        if self.estado != EstadoSprint.EN_EJECUCION:
            raise DomainError(f"Cannot close sprint in state {self.estado}")
        self.estado = EstadoSprint.FINALIZADO
        self._events.append(SprintClosed(
            sprint_id=self.id, project_id=self.project_id, closed_by=closed_by
        ))

    def cancel(self) -> None:
        self.estado = EstadoSprint.CANCELADO

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class SprintEvento:
    id: SprintEventoId
    sprint_id: SprintId
    tipo: TipoEventoScrum
    fecha: datetime
    notas: str
    duracion_minutos: int
    created_by: UserId


@dataclass
class Task:
    id: TaskId
    historia_usuario_id: HistoriaUsuarioId
    sprint_id: SprintId | None
    assigned_to: UserId | None
    titulo: str
    descripcion: str
    estado: EstadoTarea
    fecha_creacion: datetime
    fecha_limite: date | None
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        historia_usuario_id: HistoriaUsuarioId,
        titulo: str,
        descripcion: str,
        sprint_id: SprintId | None = None,
        assigned_to: UserId | None = None,
        fecha_limite: date | None = None,
    ) -> Task:
        return Task(
            id=TaskId.generate(),
            historia_usuario_id=historia_usuario_id,
            sprint_id=sprint_id,
            assigned_to=assigned_to,
            titulo=titulo,
            descripcion=descripcion,
            estado=EstadoTarea.PENDIENTE,
            fecha_creacion=datetime.now(),
            fecha_limite=fecha_limite,
        )

    def assign_to(self, user_id: UserId) -> None:
        self.assigned_to = user_id

    def move_to(self, new_estado: EstadoTarea, user_id: UserId) -> None:
        old_estado = self.estado
        self.estado = new_estado
        self._events.append(TaskMoved(
            task_id=self.id, from_estado=old_estado, to_estado=new_estado, user_id=user_id
        ))

    def block(self, reason: str, blocked_by: UserId) -> None:
        self.estado = EstadoTarea.BLOQUEADO
        self._events.append(TaskBlocked(task_id=self.id, reason=reason, blocked_by=blocked_by))

    def unblock(self) -> None:
        if self.estado == EstadoTarea.BLOQUEADO:
            self.estado = EstadoTarea.EN_PROCESO

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class TaskStateTransition:
    id: str
    task_id: TaskId
    from_estado: EstadoTarea
    to_estado: EstadoTarea
    timestamp: datetime
    user_id: UserId
    reason: str | None


@dataclass
class Message:
    id: MessageId
    proyecto_id: ProjectId | None
    task_id: TaskId | None
    sender_id: UserId
    contenido: str
    fecha_envio: datetime
    tipo: TipoMensaje

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def send(
        contenido: str,
        sender_id: UserId,
        tipo: TipoMensaje,
        proyecto_id: ProjectId | None = None,
        task_id: TaskId | None = None,
    ) -> Message:
        msg = Message(
            id=MessageId.generate(),
            proyecto_id=proyecto_id,
            task_id=task_id,
            sender_id=sender_id,
            contenido=contenido,
            fecha_envio=datetime.now(),
            tipo=tipo,
        )
        msg._events.append(MessageSent(message_id=msg.id, sender_id=sender_id, tipo=tipo))
        return msg

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class Artifact:
    id: ArtifactId
    task_id: TaskId
    nombre: str
    tipo: TipoArtefacto
    version_actual: int
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(task_id: TaskId, nombre: str, tipo: TipoArtefacto) -> Artifact:
        artifact = Artifact(
            id=ArtifactId.generate(),
            task_id=task_id,
            nombre=nombre,
            tipo=tipo,
            version_actual=1,
        )
        artifact._events.append(ArtifactUploaded(
            artifact_id=artifact.id, task_id=task_id, nombre=nombre, tipo=tipo
        ))
        return artifact

    def new_version(self) -> int:
        self.version_actual += 1
        return self.version_actual

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events


@dataclass
class ArtifactVersion:
    id: ArtifactVersionId
    artifact_id: ArtifactId
    version: int
    content_url: str
    uploaded_by: UserId
    created_at: datetime
