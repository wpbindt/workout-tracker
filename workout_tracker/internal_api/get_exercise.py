from dataclasses import dataclass
from uuid import UUID

from workout_tracker.models.exercise import Exercise
from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import Request, RequestExecutor


@dataclass
class GetExercise(Request[Exercise]):
    exercise_id: UUID


class GetExerciseExecutor(RequestExecutor[GetExercise, Exercise]):
    async def execute(
        self,
        request: GetExercise,
        repositories: Repositories
    ) -> Exercise:
        return (await repositories.exercise.get_by_ids({request.exercise_id}))[request.exercise_id]
