from __future__ import annotations

from app.domain.entities.project_assignment import ProjectAssignment
from app.domain.enums import Rol
from app.domain.repositories.i_project_assignment_repository import IProjectAssignmentRepository
from app.domain.repositories.i_user_repository import IUserRepository
from app.domain.value_objects import ProjectId, UserId
from app.domain.value_objects import ProjectId as IdGen


class AssignTeamUseCase:
    def __init__(
        self, assignment_repo: IProjectAssignmentRepository,
        user_repo: IUserRepository,
    ):
        self._assignment_repo = assignment_repo
        self._user_repo = user_repo

    async def execute(
        self, project_id: ProjectId, user_id: UserId, rol: Rol,
    ) -> ProjectAssignment:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if rol not in (Rol.SCRUM_MASTER, Rol.DEVELOPER):
            raise ValueError("Invalid role for assignment")

        assignment = ProjectAssignment(
            id=str(IdGen.generate()),
            project_id=project_id,
            user_id=user_id,
            rol=rol,
        )
        await self._assignment_repo.save(assignment)
        return assignment
