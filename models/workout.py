from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from models.exercise import RepUnit, DifficultyUnit


class Reps(BaseModel):
    amount: Decimal
    unit: RepUnit


class Difficulty(BaseModel):
    amount: Decimal
    unit: DifficultyUnit


class WrongDifficultyUnit(Exception):
    pass


class WrongRepUnit(Exception):
    pass


class Set(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    exercise_id: UUID
    intended_reps: Reps
    actual_reps: Reps
    difficulty: Difficulty

    def __post_init__(self) -> None:
        if self.actual_reps.unit != self.intended_reps.unit:
            raise WrongRepUnit


class Workout(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    time: datetime = Field(default_factory=datetime.now)
    sets: list[Set] = Field(default_factory=list)
