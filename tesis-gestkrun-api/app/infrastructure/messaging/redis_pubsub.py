from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import redis.asyncio as aioredis

from app.core.config import settings


class RedisPubSub:
    def __init__(self) -> None:
        self._client: aioredis.Redis | None = None
        self._pubsub: aioredis.client.PubSub | None = None

    async def connect(self) -> None:
        if self._client is None:
            self._client = await aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            self._pubsub = self._client.pubsub()

    async def disconnect(self) -> None:
        if self._pubsub:
            await self._pubsub.close()
        if self._client:
            await self._client.close()
            self._client = None

    async def publish(self, channel: str, message: dict[str, Any]) -> None:
        if not self._client:
            return
        await self._client.publish(channel, json.dumps(message, default=str))

    async def subscribe(self, channel: str, callback: Callable[[dict[str, Any]], None]) -> None:
        if not self._pubsub:
            return

        async def _handler(msg: dict[str, Any]) -> None:
            if msg["type"] == "message":
                try:
                    data = json.loads(msg["data"])
                    callback(data)
                except (json.JSONDecodeError, KeyError):
                    pass

        await self._pubsub.subscribe(**{channel: _handler})

    async def unsubscribe(self, channel: str) -> None:
        if not self._pubsub:
            return
        await self._pubsub.unsubscribe(channel)

    async def listen(self) -> None:
        if not self._pubsub:
            return
        async for _message in self._pubsub.listen():
            pass
