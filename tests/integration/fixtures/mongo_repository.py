import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from tests.integration.fixtures.test_object import TestObject
from workout_tracker.adapters.repositories.mongo_repository import MongoRepository
from workout_tracker.adapters.repositories.serializers import serialize, deserialize


@pytest_asyncio.fixture
async def mongo_repository():
    mongo_client = AsyncIOMotorClient('mongodb://mongo:27017/?uuidRepresentation=standard')
    yield MongoRepository(
        mongo_client,
        database='test_database',
        collection='test_collection',
        serialize_entity=serialize,
        deserialize_entity=lambda value: deserialize(value, target_type=TestObject),
    )
    await mongo_client.test_database.test_collection.drop()
