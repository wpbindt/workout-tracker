from dataclasses import dataclass
from uuid import UUID

from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import Request, RequestExecutor
from workout_tracker.models.workout import Set


@dataclass(frozen=True)
class AddSet(Request[UUID]):
    workout_id: UUID
    set_: Set


class AddSetExecutor(RequestExecutor[AddSet, Set]):
    async def execute(
        self,
        request: AddSet,
        repositories: Repositories
    ) -> UUID:
        workout = (await repositories.workout.get_by_ids({request.workout_id}))[request.workout_id]
        workout.sets.append(request.set_)
        await repositories.workout.add(workout)
        return request.set_.id
