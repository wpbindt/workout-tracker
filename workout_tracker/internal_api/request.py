from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

if typing.TYPE_CHECKING:
    from workout_tracker.app import App
from workout_tracker.repositories.repository import Repositories

ResponseType = TypeVar('ResponseType')


class Request(Generic[ResponseType]):
    async def execute(self, app: App) -> ResponseType:
        return await app.execute(self)


RequestType = TypeVar('RequestType')


class RequestExecutor(ABC, Generic[RequestType, ResponseType]):
    @abstractmethod
    async def execute(
        self,
        request: RequestType,
        repositories: Repositories,
    ) -> ResponseType:
        ...
