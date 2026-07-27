from __future__ import annotations

import shutil
from pathlib import Path

from app.core.config import settings


class FileStorage:
    def __init__(self, base_path: str | None = None) -> None:
        self._base_path = Path(base_path or settings.storage_path or "/tmp/gestkrun-storage")
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _artifact_path(self, artifact_id: str, version: int) -> Path:
        return self._base_path / artifact_id / str(version)

    def store(self, artifact_id: str, version: int, content: bytes, filename: str) -> str:
        dest_dir = self._base_path / artifact_id / str(version)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename
        dest_path.write_bytes(content)
        return str(dest_path)

    def retrieve(self, artifact_id: str, version: int) -> bytes | None:
        artifact_dir = self._base_path / artifact_id / str(version)
        if not artifact_dir.exists():
            return None
        files = list(artifact_dir.iterdir())
        if not files:
            return None
        return files[0].read_bytes()

    def delete(self, artifact_id: str) -> bool:
        artifact_dir = self._base_path / artifact_id
        if not artifact_dir.exists():
            return False
        shutil.rmtree(artifact_dir)
        return True

    def exists(self, artifact_id: str, version: int) -> bool:
        return (self._base_path / artifact_id / str(version)).exists()
