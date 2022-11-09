from workout_tracker.api.get_set import GetSet
from workout_tracker.api.models.workout import Set
from workout_tracker.api.request import RequestExecutor, ResponseType
from workout_tracker.repositories.repository import Repositories


class GetSetExecutor(RequestExecutor[GetSet, Set]):
    async def execute(
        self,
        request: GetSet,
        repositories: Repositories
    ) -> ResponseType:
        workout = (await repositories.workout.get_by_ids({request.workout_id}))[request.workout_id]
        matches = [set_ for set_ in workout.sets if set_.id == request.set_id]
        if len(matches) > 0:
            return next(iter(matches))
        raise ValueError
