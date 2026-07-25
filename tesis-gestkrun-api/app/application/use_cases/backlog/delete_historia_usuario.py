from __future__ import annotations

from app.domain.repositories.i_historia_usuario_repository import IHistoriaUsuarioRepository
from app.domain.value_objects import HistoriaUsuarioId


class DeleteHistoriaUsuarioUseCase:
    def __init__(self, repo: IHistoriaUsuarioRepository):
        self._repo = repo

    async def execute(self, historia_id: HistoriaUsuarioId) -> bool:
        hu = await self._repo.get_by_id(historia_id)
        if not hu:
            return False
        await self._repo.delete(historia_id)
        return True
