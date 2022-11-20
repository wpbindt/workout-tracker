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
        documents = await self._collection.find({'_id': {'$in': list(ids)}}).to_list(len(ids))
        return {
            document['_id']: self._deserialize_entity(document['value'])
            for document in documents
        }

    async def add(self, entity: Entity) -> None:
        await self._collection.replace_one(
            filter={'_id': entity.id},
            replacement={
                '_id': entity.id,
                'value': self._serialize_entity(entity)
            },
            upsert=True,
        )

    async def get_all(self) -> AsyncIterator[Entity]:
        async for document in self._collection.find():
            yield self._deserialize_entity(document['value'])

    async def remove(self, entity_id: EntityId) -> None:
        await self._collection.delete_one({'_id': entity_id})
