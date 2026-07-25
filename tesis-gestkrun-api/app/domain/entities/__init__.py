from __future__ import annotations

from app.domain.entities.artifact import Artifact
from app.domain.entities.artifact_version import ArtifactVersion
from app.domain.entities.epica import Epica
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.entities.message import Message
from app.domain.entities.module import Module
from app.domain.entities.module_developer import ModuleDeveloper
from app.domain.entities.project import Project
from app.domain.entities.project_assignment import ProjectAssignment
from app.domain.entities.sprint import Sprint
from app.domain.entities.sprint_evento import SprintEvento
from app.domain.entities.task import Task
from app.domain.entities.task_state_transition import TaskStateTransition
from app.domain.entities.user import User

__all__ = [
    "User", "Project", "ProjectAssignment", "Module", "ModuleDeveloper",
    "Epica", "HistoriaUsuario", "Sprint", "SprintEvento",
    "Task", "TaskStateTransition", "Message", "Artifact", "ArtifactVersion",
]
