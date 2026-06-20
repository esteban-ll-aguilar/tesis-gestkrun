from datetime import datetime

from app.domain.entities import Task
from app.domain.enums import EstadoTarea
from app.domain.events import WIPViolated
from app.domain.value_objects import UserId


class WIPValidationService:
    MAX_WIP = 3

    def validate(self, user_id: UserId, current_in_progress: int) -> WIPViolated | None:
        if current_in_progress >= self.MAX_WIP:
            return WIPViolated(
                user_id=user_id, current_count=current_in_progress, max_allowed=self.MAX_WIP
            )
        return None

    def can_take_task(self, user_id: UserId, current_in_progress: int) -> bool:
        return current_in_progress < self.MAX_WIP


class KanbanFlowService:
    VALID_TRANSITIONS = {
        EstadoTarea.PENDIENTE: {EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO},
        EstadoTarea.EN_PROCESO: {
            EstadoTarea.BLOQUEADO, EstadoTarea.EN_REVISION, EstadoTarea.CANCELADO,
        },
        EstadoTarea.BLOQUEADO: {EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO},
        EstadoTarea.EN_REVISION: {
            EstadoTarea.TERMINADO, EstadoTarea.EN_PROCESO, EstadoTarea.CANCELADO,
        },
        EstadoTarea.TERMINADO: set(),
        EstadoTarea.CANCELADO: set(),
    }

    def can_transition(self, task: Task, to_estado: EstadoTarea) -> bool:
        return to_estado in self.VALID_TRANSITIONS.get(task.estado, set())

    def get_allowed_transitions(self, task: Task) -> list[EstadoTarea]:
        return sorted(
            self.VALID_TRANSITIONS.get(task.estado, set()), key=lambda x: x.value
        )

    def is_terminal(self, estado: EstadoTarea) -> bool:
        return estado in {EstadoTarea.TERMINADO, EstadoTarea.CANCELADO}


class MetricsCalculationService:
    def calculate_lead_time(self, created_at: datetime, completed_at: datetime) -> float:
        delta = completed_at - created_at
        return max(0, delta.total_seconds() / 3600)

    def calculate_cycle_time(self, started_at: datetime, completed_at: datetime) -> float:
        delta = completed_at - started_at
        return max(0, delta.total_seconds() / 3600)

    def calculate_throughput(self, completed_count: int, period_days: float) -> float:
        if period_days <= 0:
            return 0.0
        return completed_count / period_days

    def calculate_velocity_percentage(
        self, planned_points: int, completed_points: int,
    ) -> float:
        if planned_points == 0:
            return 0.0
        return (completed_points / planned_points) * 100
