from __future__ import annotations

from app.application.dto.backlog import HistoriaUsuarioResult
from app.application.mappers.backlog_mapper import historia_to_result
from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.value_objects import EpicaId


class ListHistoriasUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(self, epica_id: EpicaId) -> list[HistoriaUsuarioResult]:
        historias = await self._repo.list_by_epica(epica_id)
        return [historia_to_result(h) for h in historias]
