from typing import AsyncIterator, Any, Callable

from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient

from workout_tracker.repositories.repository import Repository, Entity, EntityId


class MongoRepository(Repository[Entity, EntityId]):
    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,
        database: str,
        collection: str,
        serialize_entity: Callable[[Entity], dict[str, Any]],
        deserialize_entity: Callable[[dict[str, Any]], Entity],
    ) -> None:
        self._collection: AgnosticCollection = mongo_client[database][collection]
        self._serialize_entity = serialize_entity
        self._deserialize_entity = deserialize_entity

    async def get_by_ids(self, ids: set[EntityId]) -> dict[EntityId, Entity]:
        output = {}
        for id_ in ids:
            raw = await self._collection.find_one(id_)
            if raw is None:
                continue
            output[id_] = self._deserialize_entity(raw['value'])
        return output

    async def add(self, entity: Entity) -> None:
        await self._collection.insert_one({'_id': entity.id, 'value': self._serialize_entity(entity)})

    async def get_all(self) -> AsyncIterator[Entity]:
        async for raw in self._collection.find():
            yield self._deserialize_entity(raw['value'])
