from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class FixtureEnum(Enum):
    A = 0
    B = 1


class FixtureObject(BaseModel):
    id: UUID
    value: str
    other_value: int
    test_enum: FixtureEnum = FixtureEnum.A

    class Config:
        frozen = True
