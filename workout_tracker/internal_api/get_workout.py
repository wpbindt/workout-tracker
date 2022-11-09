from dataclasses import dataclass
from uuid import UUID

from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import ResponseType, Request, RequestExecutor
from workout_tracker.models.workout import Workout


@dataclass
class GetWorkout(Request[Workout]):
    workout_id: UUID


class GetWorkoutExecutor(RequestExecutor[GetWorkout, Workout]):
    async def execute(
        self,
        request: GetWorkout,
        repositories: Repositories
    ) -> ResponseType:
        return (await repositories.workout.get_by_ids({request.workout_id}))[request.workout_id]
