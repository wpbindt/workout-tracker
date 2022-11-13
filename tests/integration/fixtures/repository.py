from __future__ import annotations
from uuid import UUID

import pytest

from tests.integration.fixtures.test_object import TestObject
from workout_tracker.repositories.repository import Repository


@pytest.fixture(params=[
    'fake_repository',
    'mongo_repository',
])
def repository(request) -> Repository[TestObject, UUID]:
    return request.getfixturevalue(request.param)
