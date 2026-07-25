from datetime import date, datetime

from app.domain.entities.artifact import Artifact, ArtifactVersion
from app.domain.entities.epica import Epica
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.entities.message import Message
from app.domain.entities.sprint import Sprint
from app.domain.entities.sprint_evento import SprintEvento
from app.domain.entities.task import Task, TaskStateTransition
from app.domain.enums import (
    EstadoSprint,
    EstadoTarea,
    Prioridad,
    TipoArtefacto,
    TipoEventoScrum,
    TipoMensaje,
)
from app.domain.value_objects import (
    ArtifactId,
    ArtifactVersionId,
    EpicaId,
    EstimacionEsfuerzo,
    HistoriaUsuarioId,
    ModuleId,
    ProjectId,
    SprintEventoId,
    SprintId,
    TaskId,
    UserId,
)


class TestSprintEntity:
    def test_plan_sprint(self):
        project_id = ProjectId.generate()
        sprint = Sprint.plan(
            project_id=project_id,
            nombre="Sprint 1",
            objetivo="Completar login",
            duracion_dias=14,
            fecha_inicio=date(2025, 1, 1),
        )
        assert sprint.estado == EstadoSprint.PLANIFICADO
        assert sprint.nombre == "Sprint 1"
        assert sprint.fecha_fin == date(2025, 1, 15)
        assert len(sprint._events) == 1

    def test_start_sprint(self):
        project_id = ProjectId.generate()
        sprint = Sprint.plan(project_id, "Sprint 1", "", 14, date.today())
        sprint.start()
        assert sprint.estado == EstadoSprint.EN_EJECUCION

    def test_start_sprint_invalid_state(self):
        project_id = ProjectId.generate()
        sprint = Sprint.plan(project_id, "Sprint 1", "", 14, date.today())
        sprint.start()
        import pytest

        from app.domain.value_objects import DomainError
        with pytest.raises(DomainError):
            sprint.start()

    def test_close_sprint(self):
        project_id = ProjectId.generate()
        user_id = UserId.generate()
        sprint = Sprint.plan(project_id, "Sprint 1", "", 14, date.today())
        sprint.start()
        sprint.close(user_id)
        assert sprint.estado == EstadoSprint.FINALIZADO
        assert len(sprint._events) == 2

    def test_cancel_sprint(self):
        sprint = Sprint.plan(ProjectId.generate(), "Sprint 1", "", 14, date.today())
        sprint.cancel()
        assert sprint.estado == EstadoSprint.CANCELADO


class TestEpicaEntity:
    def test_create_epica(self):
        epica = Epica.create(
            ProjectId.generate(), "Login", "Login module", Prioridad.ALTA, 1
        )
        assert epica.titulo == "Login"
        assert epica.prioridad == Prioridad.ALTA
        assert epica.estado == "ACTIVA"
        assert epica.orden == 1

    def test_epica_ordering(self):
        e1 = Epica.create(ProjectId.generate(), "A", "", Prioridad.MEDIA, 1)
        e2 = Epica.create(ProjectId.generate(), "B", "", Prioridad.MEDIA, 2)
        assert e1.orden < e2.orden


class TestHistoriaUsuarioEntity:
    def test_create_historia(self):
        hu = HistoriaUsuario.create(
            EpicaId.generate(), "Login form", "As a user...",
            "Given...", Prioridad.ALTA, EstimacionEsfuerzo(5), 1,
        )
        assert hu.titulo == "Login form"
        assert int(hu.estimacion) == 5
        assert hu.orden == 1

    def test_create_historia_with_module(self):
        hu = HistoriaUsuario.create(
            EpicaId.generate(), "Test", "", "", Prioridad.BAJA,
            EstimacionEsfuerzo(1), 1, ModuleId.generate(),
        )
        assert hu.modulo_id is not None


class TestTaskEntity:
    def test_create_task(self):
        task = Task.create(
            HistoriaUsuarioId.generate(), "Implement login",
            "Create login UI",
        )
        assert task.estado == EstadoTarea.PENDIENTE
        assert task.assigned_to is None

    def test_assign_task(self):
        task = Task.create(HistoriaUsuarioId.generate(), "Test", "")
        user_id = UserId.generate()
        task.assign_to(user_id)
        assert task.assigned_to == user_id

    def test_move_task(self):
        task = Task.create(HistoriaUsuarioId.generate(), "Test", "")
        user_id = UserId.generate()
        task.move_to(EstadoTarea.EN_PROCESO, user_id)
        assert task.estado == EstadoTarea.EN_PROCESO
        assert len(task._events) == 1

    def test_block_task(self):
        task = Task.create(HistoriaUsuarioId.generate(), "Test", "")
        task.move_to(EstadoTarea.EN_PROCESO, UserId.generate())
        task.block("Missing dependency", UserId.generate())
        assert task.estado == EstadoTarea.BLOQUEADO

    def test_unblock_task(self):
        task = Task.create(HistoriaUsuarioId.generate(), "Test", "")
        task.move_to(EstadoTarea.EN_PROCESO, UserId.generate())
        task.block("Reason", UserId.generate())
        task.unblock()
        assert task.estado == EstadoTarea.EN_PROCESO


class TestMessageEntity:
    def test_send_message(self):
        msg = Message.send(
            "Hello team", UserId.generate(), TipoMensaje.PROYECTO,
            proyecto_id=ProjectId.generate(),
        )
        assert msg.contenido == "Hello team"
        assert msg.tipo == TipoMensaje.PROYECTO

    def test_send_task_message(self):
        msg = Message.send(
            "Task update", UserId.generate(), TipoMensaje.TAREA,
            task_id=TaskId.generate(),
        )
        assert msg.tipo == TipoMensaje.TAREA
        assert msg.task_id is not None


class TestArtifactEntity:
    def test_create_artifact(self):
        artifact = Artifact.create(
            TaskId.generate(), "diagram.png", TipoArtefacto.DIAGRAMA
        )
        assert artifact.nombre == "diagram.png"
        assert artifact.version_actual == 1
        assert len(artifact._events) == 1

    def test_new_version(self):
        artifact = Artifact.create(
            TaskId.generate(), "doc.pdf", TipoArtefacto.DOCUMENTO
        )
        v = artifact.new_version()
        assert v == 2
        assert artifact.version_actual == 2

    def test_new_version_multiple(self):
        artifact = Artifact.create(
            TaskId.generate(), "code.py", TipoArtefacto.CODIGO
        )
        artifact.new_version()
        artifact.new_version()
        assert artifact.version_actual == 3


class TestSprintEventoEntity:
    def test_create_evento(self):
        evento = SprintEvento(
            id=SprintEventoId.generate(),
            sprint_id=SprintId.generate(),
            tipo=TipoEventoScrum.DAILY_SCRUM,
            fecha=datetime.now(),
            notas="Daily standup",
            duracion_minutos=15,
            created_by=UserId.generate(),
        )
        assert evento.tipo == TipoEventoScrum.DAILY_SCRUM
        assert evento.notas == "Daily standup"


class TestTaskStateTransitionEntity:
    def test_create_transition(self):
        transition = TaskStateTransition(
            id="test-id",
            task_id=TaskId.generate(),
            from_estado=EstadoTarea.PENDIENTE,
            to_estado=EstadoTarea.EN_PROCESO,
            timestamp=datetime.now(),
            user_id=UserId.generate(),
            reason="Starting work",
        )
        assert transition.from_estado == EstadoTarea.PENDIENTE
        assert transition.to_estado == EstadoTarea.EN_PROCESO
        assert transition.reason == "Starting work"


class TestArtifactVersionEntity:
    def test_create_version(self):
        version = ArtifactVersion(
            id=ArtifactVersionId.generate(),
            artifact_id=ArtifactId.generate(),
            version=1,
            content_url="/uploads/test.pdf",
            uploaded_by=UserId.generate(),
            created_at=datetime.now(),
        )
        assert version.version == 1
        assert version.content_url == "/uploads/test.pdf"
