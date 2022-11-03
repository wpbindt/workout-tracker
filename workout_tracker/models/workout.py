from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from workout_tracker.models.exercise import RepUnit, DifficultyUnit


class Reps(BaseModel):
    amount: Decimal
    unit: RepUnit


class Difficulty(BaseModel):
    amount: Decimal
    unit: DifficultyUnit


class Set(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    exercise_id: UUID
    intended_reps: Reps
    actual_reps: Reps
    difficulty: Difficulty


class Workout(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    time: datetime = Field(default_factory=datetime.now)
    sets: list[Set] = Field(default_factory=list)
