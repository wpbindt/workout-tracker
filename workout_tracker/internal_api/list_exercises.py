from dataclasses import dataclass
from uuid import UUID

from workout_tracker.models.exercise import Exercise
from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import Request, RequestExecutor


@dataclass
class ListExercises(Request[dict[UUID, Exercise]]):
    pass


class ListExercisesExecutor(RequestExecutor[ListExercises, dict[UUID, Exercise]]):
    async def execute(
        self,
        request: ListExercises,
        repositories: Repositories
    ) -> dict[UUID, Exercise]:
        return {
            exercise.id: exercise
            async for exercise in repositories.exercise.get_all()
        }
