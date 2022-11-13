import datetime
from decimal import Decimal
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
    decimal_value: Decimal


class TestObject(BaseModel):
    integer_value: int
    date_time_value: datetime.datetime
    string_value: str
    decimal_value: Decimal
    enum_value: TestEnum
    uuid_value: UUID
    nested_objects: list[NestedObject]


@pytest.fixture
def serialization_test_object() -> TestObject:
    return TestObject(
        integer_value=3,
        date_time_value=datetime.datetime.now(),
        string_value='three',
        enum_value=TestEnum.B,
        decimal_value=Decimal('9.50'),
        uuid_value=uuid4(),
        nested_objects=[
            NestedObject(
                float_value=3.50,
                int_value=9,
                enum_value=TestEnum.A,
                decimal_value=Decimal('10.50'),
            ),
            NestedObject(
                float_value=4.50,
                int_value=7,
                enum_value=TestEnum.B,
                decimal_value=Decimal('11.50'),
            ),
        ]
    )


def test_serializing_and_deserializing_are_inverse(serialization_test_object: TestObject) -> None:
    deserialized = deserialize(
        serialize(
            serialization_test_object
        ),
        target_type=TestObject,
    )

    assert deserialized == serialization_test_object
