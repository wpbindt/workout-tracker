from dataclasses import dataclass
from uuid import UUID

from workout_tracker.api.models.workout import Workout
from workout_tracker.api.request import Request


@dataclass
class GetWorkout(Request[Workout]):
    workout_id: UUID
