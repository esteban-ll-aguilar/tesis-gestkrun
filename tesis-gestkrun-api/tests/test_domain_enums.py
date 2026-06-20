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


class TestRol:
    def test_values(self):
        assert Rol.ADMIN == "ADMIN"
        assert Rol.PRODUCT_OWNER == "PRODUCT_OWNER"
        assert Rol.SCRUM_MASTER == "SCRUM_MASTER"
        assert Rol.DEVELOPER == "DEVELOPER"


class TestEstadoTarea:
    def test_values(self):
        assert EstadoTarea.PENDIENTE == "PENDIENTE"
        assert EstadoTarea.EN_PROCESO == "EN_PROCESO"
        assert EstadoTarea.BLOQUEADO == "BLOQUEADO"
        assert EstadoTarea.EN_REVISION == "EN_REVISION"
        assert EstadoTarea.TERMINADO == "TERMINADO"
        assert EstadoTarea.CANCELADO == "CANCELADO"


class TestEstadoSprint:
    def test_values(self):
        assert EstadoSprint.PLANIFICADO == "PLANIFICADO"
        assert EstadoSprint.EN_EJECUCION == "EN_EJECUCION"
        assert EstadoSprint.FINALIZADO == "FINALIZADO"
        assert EstadoSprint.CANCELADO == "CANCELADO"


class TestEstadoProyecto:
    def test_values(self):
        assert EstadoProyecto.ACTIVO == "ACTIVO"
        assert EstadoProyecto.INACTIVO == "INACTIVO"
        assert EstadoProyecto.FINALIZADO == "FINALIZADO"
        assert EstadoProyecto.CANCELADO == "CANCELADO"


class TestPrioridad:
    def test_values(self):
        assert Prioridad.BAJA == "BAJA"
        assert Prioridad.MEDIA == "MEDIA"
        assert Prioridad.ALTA == "ALTA"
        assert Prioridad.CRITICA == "CRITICA"


class TestTipoEventoScrum:
    def test_values(self):
        assert TipoEventoScrum.SPRINT_PLANNING == "SPRINT_PLANNING"
        assert TipoEventoScrum.DAILY_SCRUM == "DAILY_SCRUM"
        assert TipoEventoScrum.SPRINT_REVIEW == "SPRINT_REVIEW"
        assert TipoEventoScrum.SPRINT_RETROSPECTIVE == "SPRINT_RETROSPECTIVE"


class TestTipoArtefacto:
    def test_values(self):
        assert TipoArtefacto.REQUISITO == "REQUISITO"
        assert TipoArtefacto.DIAGRAMA == "DIAGRAMA"


class TestTipoMensaje:
    def test_values(self):
        assert TipoMensaje.PROYECTO == "PROYECTO"
        assert TipoMensaje.TAREA == "TAREA"


class TestEstadoModulo:
    def test_values(self):
        assert EstadoModulo.ACTIVO == "ACTIVO"
        assert EstadoModulo.INACTIVO == "INACTIVO"
