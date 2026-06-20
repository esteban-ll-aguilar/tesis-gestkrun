from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domain.entities import Epica, HistoriaUsuario, Sprint, SprintEvento
from app.domain.enums import Prioridad, TipoEventoScrum
from app.domain.repositories import (
    IEpicaRepository,
    IHistoriaUsuarioRepository,
    ISprintEventoRepository,
    ISprintRepository,
)
from app.domain.value_objects import (
    EpicaId,
    EstimacionEsfuerzo,
    HistoriaUsuarioId,
    ModuleId,
    ProjectId,
    SprintEventoId,
    SprintId,
    UserId,
)


@dataclass
class EpicaResult:
    id: str
    project_id: str
    titulo: str
    descripcion: str
    prioridad: str
    estado: str
    orden: int


@dataclass
class HistoriaUsuarioResult:
    id: str
    epica_id: str
    modulo_id: str | None
    titulo: str
    descripcion: str
    criterios_aceptacion: str
    prioridad: str
    estimacion: int
    orden: int


@dataclass
class SprintResult:
    id: str
    project_id: str
    nombre: str
    objetivo: str
    duracion_dias: int
    fecha_inicio: str
    fecha_fin: str
    estado: str


@dataclass
class SprintEventoResult:
    id: str
    sprint_id: str
    tipo: str
    fecha: str
    notas: str
    duracion_minutos: int
    created_by: str


class CreateEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(
        self, project_id: ProjectId, titulo: str, descripcion: str,
        prioridad: Prioridad,
    ) -> EpicaResult:
        max_orden = await self._repo.get_max_orden(project_id)
        epica = Epica.create(project_id, titulo, descripcion, prioridad, max_orden + 1)
        await self._repo.save(epica)
        return _epica_result(epica)


class ListEpicasUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(self, project_id: ProjectId) -> list[EpicaResult]:
        epicas = await self._repo.list_by_project(project_id)
        return [_epica_result(e) for e in epicas]


class UpdateEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(
        self, epica_id: EpicaId, titulo: str | None = None,
        descripcion: str | None = None, prioridad: Prioridad | None = None,
    ) -> EpicaResult | None:
        epica = await self._repo.get_by_id(epica_id)
        if not epica:
            return None
        if titulo is not None:
            epica.titulo = titulo
        if descripcion is not None:
            epica.descripcion = descripcion
        if prioridad is not None:
            epica.prioridad = prioridad
        await self._repo.save(epica)
        return _epica_result(epica)


class DeleteEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(self, epica_id: EpicaId) -> bool:
        epica = await self._repo.get_by_id(epica_id)
        if not epica:
            return False
        await self._repo.delete(epica_id)
        return True


class PrioritizeBacklogUseCase:
    def __init__(self, epica_repo: IEpicaRepository, hu_repo: IHistoriaUsuarioRepository):
        self._epica_repo = epica_repo
        self._hu_repo = hu_repo

    async def reorder_epicas(self, project_id: ProjectId, epica_ids: list[str]) -> None:
        for i, eid in enumerate(epica_ids):
            epica = await self._epica_repo.get_by_id(EpicaId(value=UUID(eid)))
            if epica:
                epica.orden = i + 1
                await self._epica_repo.save(epica)

    async def reorder_historias(self, epica_id: EpicaId, historia_ids: list[str]) -> None:
        for i, hid in enumerate(historia_ids):
            hu = await self._hu_repo.get_by_id(HistoriaUsuarioId(value=UUID(hid)))
            if hu:
                hu.orden = i + 1
                await self._hu_repo.save(hu)

    async def get_backlog(self, project_id: ProjectId) -> list[dict]:
        epicas = await self._epica_repo.list_by_project(project_id)
        result = []
        for e in epicas:
            historias = await self._hu_repo.list_by_epica(e.id)
            result.append({
                "epica": _epica_result(e),
                "historias": [_hu_result(h) for h in historias],
            })
        return result


class CreateHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(
        self, epica_id: EpicaId, titulo: str, descripcion: str,
        criterios_aceptacion: str, prioridad: Prioridad,
        estimacion: int, modulo_id: str | None = None,
    ) -> HistoriaUsuarioResult:
        hu = HistoriaUsuario.create(
            epica_id, titulo, descripcion, criterios_aceptacion,
            prioridad, EstimacionEsfuerzo(estimacion), 1,
            modulo_id=ModuleId(value=UUID(modulo_id)) if modulo_id else None,
        )
        await self._repo.save(hu)
        return _hu_result(hu)


class ListHistoriasUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(self, epica_id: EpicaId) -> list[HistoriaUsuarioResult]:
        historias = await self._repo.list_by_epica(epica_id)
        return [_hu_result(h) for h in historias]


class UpdateHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(
        self, historia_id: HistoriaUsuarioId, titulo: str | None = None,
        descripcion: str | None = None, criterios_aceptacion: str | None = None,
        prioridad: Prioridad | None = None, estimacion: int | None = None,
        modulo_id: str | None = None,
    ) -> HistoriaUsuarioResult | None:
        hu = await self._repo.get_by_id(historia_id)
        if not hu:
            return None
        if titulo is not None:
            hu.titulo = titulo
        if descripcion is not None:
            hu.descripcion = descripcion
        if criterios_aceptacion is not None:
            hu.criterios_aceptacion = criterios_aceptacion
        if prioridad is not None:
            hu.prioridad = prioridad
        if estimacion is not None:
            hu.estimacion = EstimacionEsfuerzo(estimacion)
        if modulo_id is not None:
            hu.modulo_id = ModuleId(value=UUID(modulo_id))
        await self._repo.save(hu)
        return _hu_result(hu)


class DeleteHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(self, historia_id: HistoriaUsuarioId) -> bool:
        hu = await self._repo.get_by_id(historia_id)
        if not hu:
            return False
        await self._repo.delete(historia_id)
        return True


class PlanSprintUseCase:
    def __init__(self, sprint_repo: ISprintRepository):
        self._sprint_repo = sprint_repo

    async def execute(
        self, project_id: ProjectId, nombre: str, objetivo: str,
        duracion_dias: int, fecha_inicio: date,
    ) -> SprintResult:
        sprint = Sprint.plan(project_id, nombre, objetivo, duracion_dias, fecha_inicio)
        await self._sprint_repo.save(sprint)
        return _sprint_result(sprint)


class ListSprintsUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, project_id: ProjectId) -> list[SprintResult]:
        sprints = await self._repo.list_by_project(project_id)
        return [_sprint_result(s) for s in sprints]


class GetSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> SprintResult | None:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            return None
        return _sprint_result(sprint)


class StartSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> SprintResult:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            raise ValueError("Sprint not found")
        sprint.start()
        await self._repo.save(sprint)
        return _sprint_result(sprint)


class CloseSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId, closed_by: UserId) -> SprintResult:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            raise ValueError("Sprint not found")
        sprint.close(closed_by)
        await self._repo.save(sprint)
        return _sprint_result(sprint)


class CancelSprintUseCase:
    def __init__(self, repo: ISprintRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> SprintResult:
        sprint = await self._repo.get_by_id(sprint_id)
        if not sprint:
            raise ValueError("Sprint not found")
        sprint.cancel()
        await self._repo.save(sprint)
        return _sprint_result(sprint)


class CreateSprintEventoUseCase:
    def __init__(self, repo: ISprintEventoRepository):
        self._repo = repo

    async def execute(
        self, sprint_id: SprintId, tipo: TipoEventoScrum, notas: str,
        duracion_minutos: int, created_by: UserId,
    ) -> SprintEventoResult:
        evento = SprintEvento(
            id=SprintEventoId.generate(),
            sprint_id=sprint_id,
            tipo=tipo,
            fecha=datetime.now(),
            notas=notas,
            duracion_minutos=duracion_minutos,
            created_by=created_by,
        )
        await self._repo.save(evento)
        return _evento_result(evento)


class ListSprintEventosUseCase:
    def __init__(self, repo: ISprintEventoRepository):
        self._repo = repo

    async def execute(self, sprint_id: SprintId) -> list[SprintEventoResult]:
        eventos = await self._repo.list_by_sprint(sprint_id)
        return [_evento_result(e) for e in eventos]


def _epica_result(e: Epica) -> EpicaResult:
    return EpicaResult(
        id=str(e.id), project_id=str(e.project_id), titulo=e.titulo,
        descripcion=e.descripcion, prioridad=e.prioridad.value,
        estado=e.estado, orden=e.orden,
    )


def _hu_result(h: HistoriaUsuario) -> HistoriaUsuarioResult:
    return HistoriaUsuarioResult(
        id=str(h.id), epica_id=str(h.epica_id),
        modulo_id=str(h.modulo_id) if h.modulo_id else None,
        titulo=h.titulo, descripcion=h.descripcion,
        criterios_aceptacion=h.criterios_aceptacion,
        prioridad=h.prioridad.value, estimacion=int(h.estimacion), orden=h.orden,
    )


def _sprint_result(s: Sprint) -> SprintResult:
    return SprintResult(
        id=str(s.id), project_id=str(s.project_id), nombre=s.nombre,
        objetivo=s.objetivo, duracion_dias=s.duracion_dias,
        fecha_inicio=s.fecha_inicio.isoformat(), fecha_fin=s.fecha_fin.isoformat(),
        estado=s.estado.value,
    )


def _evento_result(e: SprintEvento) -> SprintEventoResult:
    return SprintEventoResult(
        id=str(e.id), sprint_id=str(e.sprint_id), tipo=e.tipo.value,
        fecha=e.fecha.isoformat(), notas=e.notas,
        duracion_minutos=e.duracion_minutos, created_by=str(e.created_by),
    )
