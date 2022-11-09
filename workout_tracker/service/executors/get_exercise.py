from workout_tracker.api.get_exercise import GetExercise
from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.request import RequestExecutor
from workout_tracker.repositories.repository import Repositories


class GetExerciseExecutor(RequestExecutor[GetExercise, Exercise]):
    async def execute(
        self,
        request: GetExercise,
        repositories: Repositories
    ) -> Exercise:
        return (await repositories.exercise.get_by_ids({request.exercise_id}))[request.exercise_id]
