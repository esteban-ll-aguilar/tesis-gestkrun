import pytest

from app.domain.value_objects import (
    DomainError,
    Email,
    EstimacionEsfuerzo,
    PasswordHash,
    WIPCount,
)


class TestEmail:
    def test_valid_email(self):
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

    def test_invalid_email(self):
        with pytest.raises(DomainError, match="Invalid email format"):
            Email("not-an-email")

    def test_empty_email(self):
        with pytest.raises(DomainError, match="Invalid email format"):
            Email("")


class TestPasswordHash:
    def test_valid_hash(self):
        h = PasswordHash("a" * 32)
        assert str(h) == "a" * 32

    def test_empty_hash(self):
        with pytest.raises(DomainError, match="Invalid password hash"):
            PasswordHash("")

    def test_short_hash(self):
        with pytest.raises(DomainError, match="Invalid password hash"):
            PasswordHash("short")


class TestEstimacionEsfuerzo:
    def test_valid_values(self):
        for v in [1, 2, 3, 5, 8, 13, 21]:
            assert int(EstimacionEsfuerzo(v)) == v

    def test_invalid_value(self):
        with pytest.raises(DomainError, match="Estimacion must be in"):
            EstimacionEsfuerzo(4)

    def test_zero(self):
        with pytest.raises(DomainError, match="Estimacion must be in"):
            EstimacionEsfuerzo(0)


class TestWIPCount:
    def test_valid_values(self):
        for v in range(4):
            assert int(WIPCount(v)) == v

    def test_negative(self):
        with pytest.raises(DomainError, match="WIP count must be between"):
            WIPCount(-1)

    def test_too_high(self):
        with pytest.raises(DomainError, match="WIP count must be between"):
            WIPCount(4)

    def test_can_take_more(self):
        assert WIPCount(0).can_take_more() is True
        assert WIPCount(2).can_take_more() is True
        assert WIPCount(3).can_take_more() is False
