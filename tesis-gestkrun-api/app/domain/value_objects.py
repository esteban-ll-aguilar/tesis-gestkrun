import re
from dataclasses import dataclass
from uuid import UUID, uuid4


class DomainError(ValueError):
    pass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.value):
            raise DomainError(f"Invalid email format: {self.value}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PasswordHash:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 32:
            raise DomainError("Invalid password hash")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class EstimacionEsfuerzo:
    value: int

    FIBONACCI = frozenset({1, 2, 3, 5, 8, 13, 21})

    def __post_init__(self):
        if self.value not in self.FIBONACCI:
            raise DomainError(f"Estimacion must be in {sorted(self.FIBONACCI)}, got {self.value}")

    def __int__(self) -> int:
        return self.value


@dataclass(frozen=True)
class UserId:
    value: UUID

    @classmethod
    def generate(cls) -> "UserId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ProjectId:
    value: UUID

    @classmethod
    def generate(cls) -> "ProjectId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TaskId:
    value: UUID

    @classmethod
    def generate(cls) -> "TaskId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SprintId:
    value: UUID

    @classmethod
    def generate(cls) -> "SprintId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class EpicaId:
    value: UUID

    @classmethod
    def generate(cls) -> "EpicaId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class HistoriaUsuarioId:
    value: UUID

    @classmethod
    def generate(cls) -> "HistoriaUsuarioId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ModuleId:
    value: UUID

    @classmethod
    def generate(cls) -> "ModuleId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class MessageId:
    value: UUID

    @classmethod
    def generate(cls) -> "MessageId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SprintEventoId:
    value: UUID

    @classmethod
    def generate(cls) -> "SprintEventoId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ArtifactId:
    value: UUID

    @classmethod
    def generate(cls) -> "ArtifactId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ArtifactVersionId:
    value: UUID

    @classmethod
    def generate(cls) -> "ArtifactVersionId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class WIPCount:
    value: int
    limit: int = 3

    def __post_init__(self):
        if not (0 <= self.value <= self.limit):
            raise DomainError(f"WIP count must be between 0 and {self.limit}, got {self.value}")

    def can_take_more(self) -> bool:
        return self.value < self.limit

    def __int__(self) -> int:
        return self.value
