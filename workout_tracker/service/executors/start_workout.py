from datetime import datetime
from uuid import UUID

from workout_tracker.api.models.workout import Set, Workout
from workout_tracker.api.request import RequestExecutor
from workout_tracker.api.start_workout import StartWorkout
from workout_tracker.repositories.repository import Repositories


class StartWorkoutExecutor(RequestExecutor[StartWorkout, Set]):
    async def execute(
        self,
        request: StartWorkout,
        repositories: Repositories
    ) -> UUID:
        time = request.time if request.time is not None else datetime.now()
        workout = Workout(time=time)
        await repositories.workout.add(workout)
        return workout.id
