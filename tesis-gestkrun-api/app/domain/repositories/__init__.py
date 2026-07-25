from __future__ import annotations

from app.domain.repositories.i_artifact_repository import IArtifactRepository
from app.domain.repositories.i_artifact_version_repository import (
    IArtifactVersionRepository,
)
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.repositories.i_historia_usuario_repository import (
    IHistoriaUsuarioRepository,
)
from app.domain.repositories.i_message_repository import IMessageRepository
from app.domain.repositories.i_module_developer_repository import (
    IModuleDeveloperRepository,
)
from app.domain.repositories.i_module_repository import IModuleRepository
from app.domain.repositories.i_project_assignment_repository import (
    IProjectAssignmentRepository,
)
from app.domain.repositories.i_project_repository import IProjectRepository
from app.domain.repositories.i_sprint_evento_repository import ISprintEventoRepository
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.repositories.i_task_repository import ITaskRepository
from app.domain.repositories.i_task_state_transition_repository import (
    ITaskStateTransitionRepository,
)
from app.domain.repositories.i_user_repository import IUserRepository

__all__ = [
    "IUserRepository", "IProjectRepository", "IProjectAssignmentRepository",
    "IModuleRepository", "IModuleDeveloperRepository",
    "IEpicaRepository", "IHistoriaUsuarioRepository",
    "ISprintRepository", "ISprintEventoRepository",
    "ITaskRepository", "ITaskStateTransitionRepository",
    "IMessageRepository", "IArtifactRepository", "IArtifactVersionRepository",
]
