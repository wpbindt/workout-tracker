from dataclasses import dataclass
from uuid import UUID

from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.request import Request


@dataclass
class GetExercise(Request[Exercise]):
    exercise_id: UUID
