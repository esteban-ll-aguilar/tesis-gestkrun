from __future__ import annotations

from app.application.dto.backlog import (
    EpicaResult,
    HistoriaUsuarioResult,
    SprintEventoResult,
    SprintResult,
)
from app.domain.entities.epica import Epica
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.entities.sprint import Sprint
from app.domain.entities.sprint_evento import SprintEvento


def epica_to_result(e: Epica) -> EpicaResult:
    return EpicaResult(
        id=str(e.id), project_id=str(e.project_id), titulo=e.titulo,
        descripcion=e.descripcion, prioridad=e.prioridad.value,
        estado=e.estado, orden=e.orden,
        modulo_id=str(e.modulo_id) if e.modulo_id else None,
    )


def historia_to_result(
    h: HistoriaUsuario, sprint_id: str | None = None, sprint_nombre: str | None = None,
) -> HistoriaUsuarioResult:
    return HistoriaUsuarioResult(
        id=str(h.id), epica_id=str(h.epica_id),
        modulo_id=str(h.modulo_id) if h.modulo_id else None,
        titulo=h.titulo, descripcion=h.descripcion,
        criterios_aceptacion=h.criterios_aceptacion,
        prioridad=h.prioridad.value, estimacion=int(h.estimacion), orden=h.orden,
        sprint_id=sprint_id, sprint_nombre=sprint_nombre,
    )


def sprint_to_result(s: Sprint) -> SprintResult:
    return SprintResult(
        id=str(s.id), project_id=str(s.project_id), nombre=s.nombre,
        objetivo=s.objetivo, duracion_dias=s.duracion_dias,
        fecha_inicio=s.fecha_inicio.isoformat(), fecha_fin=s.fecha_fin.isoformat(),
        estado=s.estado.value, meeting_link=s.meeting_link,
    )


def evento_to_result(e: SprintEvento) -> SprintEventoResult:
    return SprintEventoResult(
        id=str(e.id), sprint_id=str(e.sprint_id), tipo=e.tipo.value,
        fecha=e.fecha.isoformat(), notas=e.notas,
        duracion_minutos=e.duracion_minutos, created_by=str(e.created_by),
    )
