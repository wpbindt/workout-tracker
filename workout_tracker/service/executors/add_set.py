from uuid import UUID

from workout_tracker.api.add_set import AddSet
from workout_tracker.api.models.workout import Set
from workout_tracker.api.request import RequestExecutor
from workout_tracker.repositories.repository import Repositories


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
