import dataclasses
from typing import Any

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from tests.integration.fixtures.test_object import TestObject, TestEnum
from workout_tracker.adapters.mongo_repository import MongoRepository


def serialize_for_mongo(obj: TestObject) -> dict[str, Any]:
    d = dataclasses.asdict(obj)
    d['test_enum'] = d['test_enum'].value
    return d


def deserialize_for_mongo(val: dict[str, Any]) -> TestObject:
    return TestObject(
        id=val['id'],
        value=val['value'],
        other_value=val['other_value'],
        test_enum=TestEnum(val['test_enum']),
    )


@pytest_asyncio.fixture
async def mongo_repository():
    mongo_client = AsyncIOMotorClient('mongodb://mongo:27017/?uuidRepresentation=standard')
    yield MongoRepository(
        mongo_client,
        database='test_database',
        collection='test_collection',
        serialize_entity=serialize_for_mongo,
        deserialize_entity=deserialize_for_mongo,
    )
    await mongo_client.test_database.test_collection.drop()
