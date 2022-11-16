from uuid import UUID

from workout_tracker.api.add_exercise import AddExercise
from workout_tracker.api.request import RequestExecutor
from workout_tracker.repositories.repository import Repositories


class AddExerciseExecutor(RequestExecutor[AddExercise, UUID]):
    async def execute(
        self,
        request: AddExercise,
        repositories: Repositories
    ) -> UUID:
        await repositories.exercise.add(request.exercise)
        return request.exercise.id
