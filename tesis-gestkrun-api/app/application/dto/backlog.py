from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EpicaResult:
    id: str
    project_id: str
    titulo: str
    descripcion: str
    prioridad: str
    estado: str
    orden: int
    modulo_id: str | None = None


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
    sprint_id: str | None = None
    sprint_nombre: str | None = None


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
    meeting_link: str = ""


@dataclass
class SprintEventoResult:
    id: str
    sprint_id: str
    tipo: str
    fecha: str
    notas: str
    duracion_minutos: int
    created_by: str
