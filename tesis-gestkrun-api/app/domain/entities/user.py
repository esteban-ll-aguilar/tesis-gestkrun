from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import Rol
from app.domain.events import (
    DomainEvent,
    UserDeactivated,
    UserRegistered,
    UserRoleChanged,
)
from app.domain.value_objects import Email, PasswordHash, UserId


@dataclass
class User:
    id: UserId
    nombre: str
    email: Email
    password_hash: PasswordHash
    rol: Rol
    fecha_registro: datetime
    deleted_at: datetime | None = None

    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def register(nombre: str, email: Email, password_hash: PasswordHash) -> User:
        user = User(
            id=UserId.generate(),
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=Rol.DEVELOPER,
            fecha_registro=datetime.now(),
        )
        user._events.append(UserRegistered(user_id=user.id, email=email, rol=user.rol))
        return user

    def change_role(self, new_rol: Rol, changed_by: UserId) -> None:
        old_rol = self.rol
        self.rol = new_rol
        self._events.append(UserRoleChanged(
            user_id=self.id, old_rol=old_rol, new_rol=new_rol, changed_by=changed_by
        ))

    def deactivate(self, deactivated_by: UserId) -> None:
        self.deleted_at = datetime.now()
        self._events.append(UserDeactivated(user_id=self.id, deactivated_by=deactivated_by))

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None
