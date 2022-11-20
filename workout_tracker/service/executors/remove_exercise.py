from workout_tracker.api.remove_exercise import RemoveExercise
from workout_tracker.api.request import RequestExecutor
from workout_tracker.repositories.repository import Repositories


class RemoveExerciseExecutor(RequestExecutor[RemoveExercise, None]):
    async def execute(
        self,
        request: RemoveExercise,
        repositories: Repositories
    ) -> None:
        await repositories.exercise.remove(request.exercise_id)
