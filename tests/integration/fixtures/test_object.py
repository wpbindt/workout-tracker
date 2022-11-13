from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TestEnum(Enum):
    A = 0
    B = 1


class TestObject(BaseModel):
    id: UUID
    value: str
    other_value: int
    test_enum: TestEnum = TestEnum.A

    class Config:
        frozen = True
