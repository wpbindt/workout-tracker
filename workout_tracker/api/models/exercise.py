from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RepUnit(str, Enum):
    REPETITION = 'repetition'
    SECONDS = 'second'


class DifficultyUnit(str, Enum):
    KILOGRAM = 'kg'
    MILLIMETER = 'mm'


class Exercise(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    rep_unit: RepUnit
    difficulty_unit: DifficultyUnit
