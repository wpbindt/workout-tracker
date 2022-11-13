import datetime
from enum import Enum
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel

from workout_tracker.adapters.repositories.serializers import serialize, deserialize


class TestEnum(Enum):
    A = 'a'
    B = 'bay'


class NestedObject(BaseModel):
    float_value: float
    int_value: int
    enum_value: TestEnum


class TestObject(BaseModel):
    integer_value: int
    date_time_value: datetime.datetime
    string_value: str
    enum_value: TestEnum
    uuid_value: UUID
    nested_object: NestedObject


@pytest.fixture
def serialization_test_object() -> TestObject:
    return TestObject(
        integer_value=3,
        date_time_value=datetime.datetime.now(),
        string_value='three',
        enum_value=TestEnum.B,
        uuid_value=uuid4(),
        nested_object=NestedObject(
            float_value=3.50,
            int_value=9,
            enum_value=TestEnum.A,
        )
    )


def test_serializing_and_deserializing_are_inverse(serialization_test_object: TestObject) -> None:
    deserialized = deserialize(
        serialize(
            serialization_test_object
        ),
        target_type=TestObject,
    )

    assert deserialized == serialization_test_object
