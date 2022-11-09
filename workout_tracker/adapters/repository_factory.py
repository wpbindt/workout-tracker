import json
from pathlib import Path
from typing import Callable
from uuid import UUID

from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.models.workout import Workout
from workout_tracker.repositories.repository import Repository
from workout_tracker.adapters.linux_db_repository import create_linux_db_repository

exercise_repository_factory: Callable[[], Repository[Exercise, UUID]] = create_linux_db_repository(
    db_path=Path('/srv/exercise.db'),
    entity_deserializer=lambda serialized: Exercise(**json.loads(serialized)),
    entity_serializer=lambda entity: entity.json(),
)
workout_repository_factory: Callable[[], Repository[Workout, UUID]] = create_linux_db_repository(
    db_path=Path('/srv/workout.db'),
    entity_deserializer=lambda serialized: Workout(**json.loads(serialized)),
    entity_serializer=lambda entity: entity.json(),
)
