from __future__ import annotations

from app.domain.repositories.i_epica_repository import IEpicaRepository
from app.domain.value_objects import EpicaId


class DeleteEpicaUseCase:
    def __init__(self, repo: IEpicaRepository):
        self._repo = repo

    async def execute(self, epica_id: EpicaId) -> bool:
        epica = await self._repo.get_by_id(epica_id)
        if not epica:
            return False
        await self._repo.delete(epica_id)
        return True
