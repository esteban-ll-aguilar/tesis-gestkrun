from __future__ import annotations

from app.application.dto.projects import ProjectResult
from app.domain.entities.project import Project


def project_to_result(project: Project) -> ProjectResult:
    return ProjectResult(
        id=str(project.id),
        nombre=project.nombre,
        descripcion=project.descripcion,
        estado=project.estado.value,
        owner_id=str(project.owner_id),
    )
