from uuid import UUID

from workout_tracker.api.list_exercises import ListExercises
from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.request import RequestExecutor
from workout_tracker.repositories.repository import Repositories


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
