from __future__ import annotations

from dataclasses import dataclass

from app.domain.value_objects import UserId


@dataclass
class CreateProjectDTO:
    nombre: str
    descripcion: str
    owner_id: UserId


@dataclass
class ProjectResult:
    id: str
    nombre: str
    descripcion: str
    estado: str
    owner_id: str
