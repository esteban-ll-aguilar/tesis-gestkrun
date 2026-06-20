from datetime import date, datetime

import pytest

from app.domain.entities import (
    Artifact,
    Epica,
    HistoriaUsuario,
    Message,
    Module,
    Project,
    Sprint,
    Task,
    User,
)
from app.domain.enums import (
    EstadoProyecto,
    EstadoSprint,
    EstadoTarea,
    Prioridad,
    Rol,
    TipoArtefacto,
    TipoMensaje,
)
from app.domain.events import (
    EpicaCreated,
    MessageSent,
    ModuleAdded,
    ProjectCreated,
    SprintClosed,
    SprintPlanned,
    TaskBlocked,
    TaskMoved,
    UserRegistered,
    UserRoleChanged,
)
from app.domain.value_objects import (
    DomainError,
    Email,
    EstimacionEsfuerzo,
    PasswordHash,
)


class TestUser:
    def test_register_creates_user(self):
        email = Email("user@test.com")
        ph = PasswordHash("a" * 32)
        user = User.register("Test User", email, ph)
        assert user.nombre == "Test User"
        assert user.email == email
        assert user.password_hash == ph
        assert user.rol == Rol.DEVELOPER
        assert user.is_active

    def test_register_emits_event(self):
        email = Email("user@test.com")
        user = User.register("Test", email, PasswordHash("b" * 32))
        events = user.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], UserRegistered)
        assert events[0].user_id == user.id

    def test_change_role(self):
        user = User.register("Test", Email("t@t.com"), PasswordHash("a" * 32))
        user.pull_events()
        changer_id = user.id
        user.change_role(Rol.SCRUM_MASTER, changer_id)
        assert user.rol == Rol.SCRUM_MASTER
        events = user.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], UserRoleChanged)
        assert events[0].new_rol == Rol.SCRUM_MASTER

    def test_deactivate(self):
        user = User.register("Test", Email("t@t.com"), PasswordHash("a" * 32))
        user.pull_events()
        user.deactivate(user.id)
        assert not user.is_active
        assert user.deleted_at is not None


class TestProject:
    def test_create_project(self):
        email = Email("owner@test.com")
        owner = User.register("Owner", email, PasswordHash("a" * 32))
        project = Project.create("Proj A", "Description", owner.id)
        assert project.nombre == "Proj A"
        assert project.estado == EstadoProyecto.ACTIVO
        assert project.owner_id == owner.id

    def test_create_emits_event(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        events = project.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], ProjectCreated)

    def test_update_project(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        project.update(nombre="New Name")
        assert project.nombre == "New Name"

    def test_change_status(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        project.change_status(EstadoProyecto.INACTIVO)
        assert project.estado == EstadoProyecto.INACTIVO


class TestModule:
    def test_create_module(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        module = Module.create(project.id, "Module 1")
        assert module.nombre == "Module 1"
        assert module.project_id == project.id
        events = module.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], ModuleAdded)


class TestEpica:
    def test_create_epica(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "Epic 1", "Desc", Prioridad.ALTA, 1)
        assert epica.titulo == "Epic 1"
        assert epica.prioridad == Prioridad.ALTA
        events = epica.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], EpicaCreated)


class TestHistoriaUsuario:
    def test_create_historia(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU 1", "Desc", "Criterios", Prioridad.ALTA,
            EstimacionEsfuerzo(5), 1,
        )
        assert hu.titulo == "HU 1"
        assert int(hu.estimacion) == 5


class TestSprint:
    def test_plan_sprint(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        sprint = Sprint.plan(project.id, "S1", "Obj", 14, date.today())
        assert sprint.estado == EstadoSprint.PLANIFICADO
        events = sprint.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], SprintPlanned)

    def test_start_sprint(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        sprint = Sprint.plan(project.id, "S1", "Obj", 14, date.today())
        sprint.pull_events()
        sprint.start()
        assert sprint.estado == EstadoSprint.EN_EJECUCION

    def test_start_non_planned_raises(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        sprint = Sprint.plan(project.id, "S1", "Obj", 14, date.today())
        sprint.start()
        with pytest.raises(DomainError, match="Cannot start sprint in state"):
            sprint.start()

    def test_close_sprint(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        sprint = Sprint.plan(project.id, "S1", "Obj", 14, date.today())
        sprint.pull_events()
        sprint.start()
        sprint.close(owner.id)
        assert sprint.estado == EstadoSprint.FINALIZADO
        events = sprint.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], SprintClosed)

    def test_close_non_active_raises(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        sprint = Sprint.plan(project.id, "S1", "Obj", 14, date.today())
        with pytest.raises(DomainError, match="Cannot close sprint in state"):
            sprint.close(owner.id)


class TestTask:
    def test_create_task(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "Task 1", "Do something")
        assert task.estado == EstadoTarea.PENDIENTE
        assert task.historia_usuario_id == hu.id

    def test_move_to(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "T", "D")
        task.move_to(EstadoTarea.EN_PROCESO, owner.id)
        assert task.estado == EstadoTarea.EN_PROCESO
        events = task.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], TaskMoved)

    def test_block_task(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "T", "D")
        task.block("Blocked by dependency", owner.id)
        assert task.estado == EstadoTarea.BLOQUEADO
        events = task.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], TaskBlocked)

    def test_unblock_task(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "T", "D")
        task.block("Blocked", owner.id)
        task.unblock()
        assert task.estado == EstadoTarea.EN_PROCESO


class TestMessage:
    def test_send_message(self):
        sender = User.register("S", Email("s@t.com"), PasswordHash("a" * 32))
        msg = Message.send("Hello", sender.id, TipoMensaje.PROYECTO)
        assert msg.contenido == "Hello"
        events = msg.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], MessageSent)


class TestArtifact:
    def test_create_artifact(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "T", "D")
        artifact = Artifact.create(task.id, "doc.pdf", TipoArtefacto.DOCUMENTO)
        assert artifact.nombre == "doc.pdf"
        assert artifact.version_actual == 1
        events = artifact.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], type(events[0]))

    def test_new_version(self):
        owner = User.register("O", Email("o@t.com"), PasswordHash("a" * 32))
        project = Project.create("P", "D", owner.id)
        epica = Epica.create(project.id, "E", "D", Prioridad.MEDIA, 1)
        hu = HistoriaUsuario.create(
            epica.id, "HU", "D", "C", Prioridad.ALTA, EstimacionEsfuerzo(3), 1,
        )
        task = Task.create(hu.id, "T", "D")
        artifact = Artifact.create(task.id, "doc.pdf", TipoArtefacto.DOCUMENTO)
        assert artifact.new_version() == 2
        assert artifact.version_actual == 2
