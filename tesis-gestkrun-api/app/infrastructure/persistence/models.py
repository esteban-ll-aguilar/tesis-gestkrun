from datetime import datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression

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


class Base(DeclarativeBase):
    pass


class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(36), nullable=True)


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class UserModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[Rol] = mapped_column(
        Enum(Rol, name="rol_enum", create_type=True),
        nullable=False,
        server_default="DEVELOPER",
    )
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ProjectModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoProyecto] = mapped_column(
        Enum(EstadoProyecto, name="estado_proyecto_enum", create_type=True),
        nullable=False,
        server_default="ACTIVO",
    )
    fecha_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    wip_limit: Mapped[int] = mapped_column(Integer, nullable=False, server_default="3")
    owner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )


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


class EpicaModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "epicas"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    prioridad: Mapped[Prioridad] = mapped_column(
        Enum(Prioridad, name="prioridad_enum", create_type=True),
        nullable=False,
        server_default="MEDIA",
    )
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default="ACTIVA")
    orden: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")


class HistoriaUsuarioModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "historias_usuario"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    epica_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("epicas.id"), nullable=False
    )
    modulo_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("modules.id"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    criterios_aceptacion: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=""
    )
    prioridad: Mapped[Prioridad] = mapped_column(
        Enum(Prioridad, name="prioridad_enum", create_type=False),
        nullable=False,
        server_default="MEDIA",
    )
    estimacion: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    orden: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")


class SprintModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "sprints"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    objetivo: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    duracion_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoSprint] = mapped_column(
        Enum(EstadoSprint, name="estado_sprint_enum", create_type=True),
        nullable=False,
        server_default="PLANIFICADO",
    )


class SprintEventoModel(Base):
    __tablename__ = "sprint_eventos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    sprint_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sprints.id"), nullable=False
    )
    tipo: Mapped[TipoEventoScrum] = mapped_column(
        Enum(TipoEventoScrum, name="tipo_evento_scrum_enum", create_type=True),
        nullable=False,
    )
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notas: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    duracion_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )


class TaskModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    historia_usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("historias_usuario.id"), nullable=False
    )
    sprint_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("sprints.id"), nullable=True
    )
    assigned_to: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    estado: Mapped[EstadoTarea] = mapped_column(
        Enum(EstadoTarea, name="estado_tarea_enum", create_type=True),
        nullable=False,
        server_default="PENDIENTE",
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_limite: Mapped[datetime | None] = mapped_column(Date, nullable=True)


class TaskStateTransitionModel(Base):
    __tablename__ = "task_state_transitions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=False
    )
    from_estado: Mapped[EstadoTarea] = mapped_column(
        Enum(EstadoTarea, name="estado_tarea_enum", create_type=False),
        nullable=False,
    )
    to_estado: Mapped[EstadoTarea] = mapped_column(
        Enum(EstadoTarea, name="estado_tarea_enum", create_type=False),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    proyecto_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=True
    )
    task_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=True
    )
    sender_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_envio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    tipo: Mapped[TipoMensaje] = mapped_column(
        Enum(TipoMensaje, name="tipo_mensaje_enum", create_type=True),
        nullable=False,
    )


class ArtifactModel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoArtefacto] = mapped_column(
        Enum(TipoArtefacto, name="tipo_artefacto_enum", create_type=True),
        nullable=False,
    )
    version_actual: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )


class ArtifactVersionModel(Base):
    __tablename__ = "artifact_versions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=expression.text("gen_random_uuid()")
    )
    artifact_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("artifacts.id"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_url: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_by: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
