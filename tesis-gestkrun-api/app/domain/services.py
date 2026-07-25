from datetime import datetime

from app.domain.events import WIPViolated
from app.domain.value_objects import UserId


class WIPValidationService:
    def validate(
        self, user_id: UserId, current_in_progress: int, wip_limit: int = 3
    ) -> WIPViolated | None:
        if current_in_progress >= wip_limit:
            return WIPViolated(
                user_id=user_id, current_count=current_in_progress, max_allowed=wip_limit
            )
        return None

    def can_take_task(self, user_id: UserId, current_in_progress: int, wip_limit: int = 3) -> bool:
        return current_in_progress < wip_limit


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
