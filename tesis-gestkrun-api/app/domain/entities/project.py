from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from app.domain.entities.epica import Epica
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.entities.message import Message
from app.domain.entities.module import Module
from app.domain.entities.sprint import Sprint
from app.domain.enums import EstadoProyecto, Prioridad, TipoMensaje
from app.domain.events import DomainEvent, ProjectCreated, ProjectDeleted
from app.domain.value_objects import EpicaId, EstimacionEsfuerzo, ModuleId, ProjectId, UserId


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
    _modules: list[Module] = field(default_factory=list, repr=False)
    _sprints: list[Sprint] = field(default_factory=list, repr=False)
    _epicas: list[Epica] = field(default_factory=list, repr=False)

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

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now()
        self._events.append(ProjectDeleted(project_id=self.id))

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None

    def add_module(self, nombre: str, descripcion: str = "") -> Module:
        module = Module.create(self.id, nombre, descripcion)
        self._modules.append(module)
        self._events.extend(module.pull_events())
        return module

    def plan_sprint(
        self,
        nombre: str,
        objetivo: str,
        duracion_dias: int,
        fecha_inicio: date,
        meeting_link: str = "",
    ) -> Sprint:
        sprint = Sprint.plan(self.id, nombre, objetivo, duracion_dias, fecha_inicio, meeting_link)
        self._sprints.append(sprint)
        self._events.extend(sprint.pull_events())
        return sprint

    def create_epica(
        self,
        titulo: str,
        descripcion: str,
        prioridad: Prioridad,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> Epica:
        epica = Epica.create(self.id, titulo, descripcion, prioridad, orden, modulo_id)
        self._epicas.append(epica)
        self._events.extend(epica.pull_events())
        return epica

    def create_historia(
        self,
        epica_id: EpicaId,
        titulo: str,
        descripcion: str,
        criterios_aceptacion: str,
        prioridad: Prioridad,
        estimacion: EstimacionEsfuerzo,
        orden: int,
        modulo_id: ModuleId | None = None,
    ) -> HistoriaUsuario:
        hu = HistoriaUsuario.create(
            epica_id, titulo, descripcion, criterios_aceptacion, prioridad,
            estimacion, orden, modulo_id,
        )
        self._events.extend(hu.pull_events())
        return hu

    def add_message(
        self,
        contenido: str,
        sender_id: UserId,
        tipo: str,
    ) -> Message:
        msg = Message.send(contenido, sender_id, TipoMensaje(tipo), proyecto_id=self.id)
        self._events.extend(msg.pull_events())
        return msg
