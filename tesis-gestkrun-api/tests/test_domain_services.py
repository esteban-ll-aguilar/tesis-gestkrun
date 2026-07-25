from datetime import datetime

from app.domain.services import (
    MetricsCalculationService,
    WIPValidationService,
)
from app.domain.value_objects import UserId


class TestWIPValidationService:
    def setup_method(self):
        self.service = WIPValidationService()
        self.user_id = UserId.generate()

    def test_validate_under_limit(self):
        result = self.service.validate(self.user_id, 2)
        assert result is None

    def test_validate_at_limit(self):
        result = self.service.validate(self.user_id, 3)
        assert result is not None
        assert result.current_count == 3
        assert result.max_allowed == 3

    def test_validate_custom_limit(self):
        result = self.service.validate(self.user_id, 2, wip_limit=2)
        assert result is not None
        assert result.max_allowed == 2

    def test_can_take_task_custom_limit(self):
        assert self.service.can_take_task(self.user_id, 3, wip_limit=5) is True
        assert self.service.can_take_task(self.user_id, 5, wip_limit=5) is False

    def test_can_take_task_true(self):
        assert self.service.can_take_task(self.user_id, 2) is True

    def test_can_take_task_false(self):
        assert self.service.can_take_task(self.user_id, 3) is False

    def test_validate_over_limit(self):
        result = self.service.validate(self.user_id, 4)
        assert result is not None


class TestMetricsCalculationService:
    def setup_method(self):
        self.service = MetricsCalculationService()

    def test_lead_time(self):
        created = datetime(2024, 1, 1, 8, 0)
        completed = datetime(2024, 1, 3, 8, 0)
        hours = self.service.calculate_lead_time(created, completed)
        assert hours == 48.0

    def test_cycle_time(self):
        started = datetime(2024, 1, 1, 10, 0)
        completed = datetime(2024, 1, 2, 10, 0)
        hours = self.service.calculate_cycle_time(started, completed)
        assert hours == 24.0

    def test_throughput(self):
        t = self.service.calculate_throughput(10, 5)
        assert t == 2.0

    def test_throughput_zero_period(self):
        t = self.service.calculate_throughput(10, 0)
        assert t == 0.0

    def test_velocity_percentage(self):
        pct = self.service.calculate_velocity_percentage(20, 15)
        assert pct == 75.0

    def test_velocity_zero_planned(self):
        pct = self.service.calculate_velocity_percentage(0, 15)
        assert pct == 0.0

    def test_lead_time_zero_delta(self):
        now = datetime.now()
        assert self.service.calculate_lead_time(now, now) == 0.0



