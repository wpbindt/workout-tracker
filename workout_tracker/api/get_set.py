from dataclasses import dataclass
from uuid import UUID

from workout_tracker.api.models.workout import Set
from workout_tracker.api.request import Request


@dataclass
class GetSet(Request[Set]):
    workout_id: UUID
    set_id: UUID
