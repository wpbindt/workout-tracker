import dataclasses
import json
from dbm import gnu as gnudbm
from pathlib import Path
from uuid import UUID

import pytest_asyncio

from tests.integration.fixtures.test_object import TestObject
from workout_tracker.adapters.linux_db_repository import LinuxDBRepository


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
