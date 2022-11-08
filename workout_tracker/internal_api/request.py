from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from workout_tracker.repositories.repository import Repositories

ResponseType = TypeVar('ResponseType')


class Request(Generic[ResponseType]):
    pass


RequestType = TypeVar('RequestType')


class RequestExecutor(ABC, Generic[RequestType, ResponseType]):
    @abstractmethod
    async def execute(
        self,
        request: RequestType,
        repositories: Repositories,
    ) -> ResponseType:
        ...