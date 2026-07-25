from __future__ import annotations

from uuid import UUID

from app.application.mappers.backlog_mapper import epica_to_result, historia_to_result
from app.domain.entities.historia_usuario import HistoriaUsuario
from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.repositories.i_sprint_repository import ISprintRepository
from app.domain.repositories.i_task_repository import ITaskRepository
from app.domain.value_objects import EpicaId, HistoriaUsuarioId, ProjectId


class PrioritizeBacklogUseCase:
    def __init__(
        self, epica_repo: IEpicaRepository, hu_repo: IHistoriaUsuarioRepository,
        task_repo: ITaskRepository | None = None,
        sprint_repo: ISprintRepository | None = None,
    ):
        self._epica_repo = epica_repo
        self._hu_repo = hu_repo
        self._task_repo = task_repo
        self._sprint_repo = sprint_repo

    async def reorder_epicas(self, project_id: ProjectId, epica_ids: list[str]) -> None:
        for i, eid in enumerate(epica_ids):
            epica = await self._epica_repo.get_by_id(EpicaId(value=UUID(eid)))
            if epica:
                epica.orden = i + 1
                await self._epica_repo.save(epica)

    async def reorder_historias(self, epica_id: EpicaId, historia_ids: list[str]) -> None:
        for i, hid in enumerate(historia_ids):
            hu = await self._hu_repo.get_by_id(HistoriaUsuarioId(value=UUID(hid)))
            if hu:
                hu.orden = i + 1
                await self._hu_repo.save(hu)

    async def _get_sprint_info(
        self, historias: list[HistoriaUsuario],
    ) -> dict[str, tuple[str | None, str | None]]:
        info: dict[str, tuple[str | None, str | None]] = {
            str(h.id): (None, None) for h in historias
        }
        if not self._task_repo:
            return info
        ids = [h.id for h in historias]
        tasks = await self._task_repo.list_by_historia_ids(ids)
        sprint_ids = list({t.sprint_id for t in tasks if t.sprint_id})
        sprint_map: dict[str, str] = {}
        if sprint_ids and self._sprint_repo:
            sprints = await self._sprint_repo.list_by_ids(sprint_ids)
            sprint_map = {str(s.id): s.nombre for s in sprints}
        for t in tasks:
            sid = str(t.sprint_id) if t.sprint_id else None
            sname = sprint_map.get(str(t.sprint_id)) if t.sprint_id else None
            info[str(t.historia_usuario_id)] = (sid, sname)
        return info

    async def get_backlog(self, project_id: ProjectId) -> list[dict]:
        epicas = await self._epica_repo.list_by_project(project_id)
        all_historias: list[HistoriaUsuario] = []
        for e in epicas:
            all_historias.extend(await self._hu_repo.list_by_epica(e.id))
        sprint_info = await self._get_sprint_info(all_historias)

        result = []
        for e in epicas:
            historias = await self._hu_repo.list_by_epica(e.id)
            result.append({
                "epica": epica_to_result(e),
                "historias": [
                    historia_to_result(h, sprint_info[str(h.id)][0], sprint_info[str(h.id)][1])
                    for h in historias
                ],
            })
        return result
