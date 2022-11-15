from typing import AsyncIterator
from uuid import UUID

import pytest_asyncio

from tests.integration.fixtures.test_object import FixtureObject
from workout_tracker.repositories.repository import Repository, Entity, EntityId


class FakeRepository(Repository[Entity, EntityId]):
    def __init__(self):
        self._entities = {}

    async def get_by_ids(self, ids: set[EntityId]) -> dict[EntityId, Entity]:
        return {
            id_: entity
            for id_, entity in self._entities.items()
            if id_ in ids
        }

    async def add(self, entity: Entity) -> None:
        self._entities[entity.id] = entity

    async def get_all(self) -> AsyncIterator[Entity]:
        for entity in self._entities.values():
            yield entity


@pytest_asyncio.fixture
async def fake_repository() -> FakeRepository[FixtureObject, UUID]:
    return FakeRepository()
