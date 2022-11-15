import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel

from workout_tracker.adapters.repositories.serializers import serialize, deserialize


class SerializationFixtureEnum(Enum):
    A = 'a'
    B = 'bay'


class NestedObject(BaseModel):
    float_value: float
    int_value: int
    enum_value: SerializationFixtureEnum
    decimal_value: Decimal


class FixtureObject(BaseModel):
    integer_value: int
    date_time_value: datetime.datetime
    string_value: str
    decimal_value: Decimal
    enum_value: SerializationFixtureEnum
    uuid_value: UUID
    nested_objects: list[NestedObject]


@pytest.fixture
def serialization_test_object() -> FixtureObject:
    return FixtureObject(
        integer_value=3,
        date_time_value=datetime.datetime.now(),
        string_value='three',
        enum_value=SerializationFixtureEnum.B,
        decimal_value=Decimal('9.50'),
        uuid_value=uuid4(),
        nested_objects=[
            NestedObject(
                float_value=3.50,
                int_value=9,
                enum_value=SerializationFixtureEnum.A,
                decimal_value=Decimal('10.50'),
            ),
            NestedObject(
                float_value=4.50,
                int_value=7,
                enum_value=SerializationFixtureEnum.B,
                decimal_value=Decimal('11.50'),
            ),
        ]
    )


def test_serializing_and_deserializing_are_inverse(serialization_test_object: FixtureObject) -> None:
    deserialized = deserialize(
        serialize(
            serialization_test_object
        ),
        target_type=FixtureObject,
    )

    assert deserialized == serialization_test_object
