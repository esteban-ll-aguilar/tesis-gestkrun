from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.enums import EstadoTarea


class TaskState(ABC):
    @property
    @abstractmethod
    def allowed_transitions(self) -> set[EstadoTarea]:
        ...

    def can_transition_to(self, to_estado: EstadoTarea) -> bool:
        return to_estado in self.allowed_transitions

    @property
    @abstractmethod
    def value(self) -> EstadoTarea:
        ...

    @property
    def is_terminal(self) -> bool:
        return False


class PendienteState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return {EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO}

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.PENDIENTE


class EnProcesoState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return {EstadoTarea.BLOQUEADO, EstadoTarea.EN_REVISION, EstadoTarea.CANCELADO}

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.EN_PROCESO


class BloqueadoState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return {EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO}

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.BLOQUEADO


class EnRevisionState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return {EstadoTarea.TERMINADO, EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO}

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.EN_REVISION


class TerminadoState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return set()

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.TERMINADO

    @property
    def is_terminal(self) -> bool:
        return True


class CanceladoState(TaskState):
    @property
    def allowed_transitions(self) -> set[EstadoTarea]:
        return set()

    @property
    def value(self) -> EstadoTarea:
        return EstadoTarea.CANCELADO

    @property
    def is_terminal(self) -> bool:
        return True


_STATE_REGISTRY: dict[EstadoTarea, type[TaskState]] = {
    EstadoTarea.PENDIENTE: PendienteState,
    EstadoTarea.EN_PROCESO: EnProcesoState,
    EstadoTarea.BLOQUEADO: BloqueadoState,
    EstadoTarea.EN_REVISION: EnRevisionState,
    EstadoTarea.TERMINADO: TerminadoState,
    EstadoTarea.CANCELADO: CanceladoState,
}


def get_state(estado: EstadoTarea) -> TaskState:
    cls = _STATE_REGISTRY.get(estado)
    if cls is None:
        raise ValueError(f"Unknown state: {estado}")
    return cls()
