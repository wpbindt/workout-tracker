from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from workout_tracker.api.request import Request


@dataclass(frozen=True)
class StartWorkout(Request[UUID]):
    time: datetime | None = None
