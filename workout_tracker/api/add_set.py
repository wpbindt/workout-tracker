from dataclasses import dataclass
from uuid import UUID

from workout_tracker.api.models.workout import Set
from workout_tracker.api.request import Request


@dataclass(frozen=True)
class AddSet(Request[UUID]):
    workout_id: UUID
    set_: Set
