from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Protocol, AsyncIterator
from uuid import UUID

from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.models.workout import Workout

EntityId = TypeVar('EntityId', covariant=True)


class HasId(Protocol[EntityId]):
    @property
    def id(self) -> EntityId:
        ...


Entity = TypeVar('Entity', bound=HasId)


class Repository(ABC, Generic[Entity, EntityId]):
    @abstractmethod
    async def get_by_ids(
        self,
        ids: set[EntityId],
    ) -> dict[EntityId, Entity]:
        ...

    @abstractmethod
    async def add(self, entity: Entity) -> None:
        ...

    @abstractmethod
    def get_all(self) -> AsyncIterator[Entity]:
        ...


@dataclass
class Repositories:
    workout: Repository[Workout, UUID]
    exercise: Repository[Exercise, UUID]
