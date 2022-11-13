from __future__ import annotations
import dataclasses
import json
from dataclasses import dataclass
from dbm import gnu as gnudbm
from pathlib import Path
from uuid import UUID

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from workout_tracker.adapters.linux_db_repository import LinuxDBRepository
from workout_tracker.adapters.mongo_repository import MongoRepository
from workout_tracker.repositories.repository import Repository


@dataclass(frozen=True)
class TestObject:
    id: UUID
    value: str
    other_value: int


def serialize_for_linux_db(entity: TestObject) -> str:
    return json.dumps(
        dataclasses.asdict(entity),
        default=str,
    )


def deserialize_for_linux_db(value: str) -> TestObject:
    d = json.loads(value)
    return TestObject(
        id=UUID(d['id']),
        value=d['value'],
        other_value=d['other_value'],
    )


@pytest_asyncio.fixture
async def linux_db_repository():
    db_path = Path('test_db.db')
    with gnudbm.open(db_path, 'c'):
        pass
    yield LinuxDBRepository(
        db_path=db_path,
        entity_deserializer=deserialize_for_linux_db,
        entity_serializer=serialize_for_linux_db,
    )
    db_path.unlink(missing_ok=True)


@pytest_asyncio.fixture
async def fake_repository():
    from tests.integration.fixtures.fake_repository import FakeRepository
    return FakeRepository()


@pytest_asyncio.fixture
async def mongo_repository():
    mongo_client = AsyncIOMotorClient('mongodb://mongo:27017/?uuidRepresentation=standard')
    yield MongoRepository(
        mongo_client,
        database='test_database',
        collection='test_collection',
        serialize_entity=lambda obj: dataclasses.asdict(obj),
        deserialize_entity=lambda val: TestObject(**val),
    )
    await mongo_client.test_database.test_collection.drop()


@pytest.fixture(params=[
    'linux_db_repository',
    'fake_repository',
    'mongo_repository',
])
def repository(request) -> Repository[TestObject, UUID]:
    return request.getfixturevalue(request.param)
