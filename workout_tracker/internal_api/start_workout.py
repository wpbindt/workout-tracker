from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import Request, RequestExecutor
from workout_tracker.models.workout import Set, Workout


@dataclass(frozen=True)
class StartWorkout(Request[UUID]):
    time: datetime | None


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
