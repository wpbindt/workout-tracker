from dataclasses import dataclass
from uuid import UUID

from workout_tracker.repositories.repository import Repositories
from workout_tracker.internal_api.request import ResponseType, Request, RequestExecutor
from workout_tracker.models.workout import Set


@dataclass
class GetSet(Request[Set]):
    workout_id: UUID
    set_id: UUID


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
