from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.api.models.workout import Workout
from workout_tracker.api.request import RequestExecutor, ResponseType
from workout_tracker.repositories.repository import Repositories


class GetWorkoutExecutor(RequestExecutor[GetWorkout, Workout]):
    async def execute(
        self,
        request: GetWorkout,
        repositories: Repositories
    ) -> ResponseType:
        return (await repositories.workout.get_by_ids({request.workout_id}))[request.workout_id]
