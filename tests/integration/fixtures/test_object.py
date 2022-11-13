from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class TestEnum(Enum):
    A = 0
    B = 1


@dataclass(frozen=True)
class TestObject:
    id: UUID
    value: str
    other_value: int
    test_enum: TestEnum = TestEnum.A
