from dataclasses import dataclass
from uuid import UUID

from workout_tracker.api.request import Request


@dataclass(frozen=True)
class RemoveExercise(Request[None]):
    exercise_id: UUID
