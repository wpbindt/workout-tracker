import dataclasses
import json
from dbm import gnu as gnudbm
from pathlib import Path
from uuid import UUID

import pytest_asyncio

from tests.integration.fixtures.test_object import TestObject
from workout_tracker.adapters.repositories.linux_db_repository import LinuxDBRepository


def serialize(entity: TestObject) -> str:
    return json.dumps(
        dataclasses.asdict(entity),
        default=str,
    )


def deserialize(value: str) -> TestObject:
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
        entity_serializer=lambda entity: entity.json(),
        entity_deserializer=TestObject.parse_raw,
    )
    db_path.unlink(missing_ok=True)
