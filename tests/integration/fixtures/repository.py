from __future__ import annotations
import dataclasses
import json
from dataclasses import dataclass
from dbm import gnu as gnudbm
from pathlib import Path
from uuid import UUID

import pytest

from workout_tracker.adapters.linux_db_repository import LinuxDBRepository
from workout_tracker.repositories.repository import Repository


@dataclass(frozen=True)
class TestObject:
    id: UUID
    value: str
    other_value: int

    @classmethod
    def deserialize(cls, value: str) -> TestObject:
        d = json.loads(value)
        return cls(
            id=UUID(d['id']),
            value=d['value'],
            other_value=d['other_value'],
        )

    def serialize(self) -> str:
        return json.dumps(
            dataclasses.asdict(self),
            default=str,
        )


@pytest.fixture
def linux_db_repository():
    db_path = Path('test_db.db')
    with gnudbm.open(db_path, 'c'):
        pass
    yield LinuxDBRepository(
        db_path=db_path,
        entity_deserializer=TestObject.deserialize,
        entity_serializer=lambda obj: obj.serialize()
    )
    db_path.unlink(missing_ok=True)


@pytest.fixture(params=['linux_db_repository'])
def repository(request) -> Repository[TestObject, UUID]:
    return request.getfixturevalue(request.param)
