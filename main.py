import json
from datetime import datetime
from pathlib import Path
from typing import Callable
from uuid import UUID

from fastapi import FastAPI, Depends

from models.exercise import Exercise
from models.workout import Workout, Set
from repositories.repository import create_linux_db_repository, Repository

app = FastAPI()


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


@app.post('/exercise')
async def create_exercise(
    exercise: Exercise,
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> dict[str, UUID]:
    await exercise_repository.add(exercise)
    return {'id': exercise.id}


@app.get('/exercise')
async def list_exercises(
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> list[Exercise]:
    return [
        exercise
        async for exercise in exercise_repository.get_all()
    ]


@app.get('/exercise/{exercise_id}')
async def get_exercise(
    exercise_id: UUID,
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> Exercise:
    workout = (await exercise_repository.get_by_ids({exercise_id}))[exercise_id]
    return workout


@app.post('/workout')
async def create_workout(
    time: datetime | None = None,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> dict[str, UUID]:
    workout = Workout() if time is None else Workout(time=time)
    await workout_repository.add(workout)
    return {'id': workout.id}


@app.get('/workout')
async def list_workouts(
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> list[Workout]:
    return [
        workout
        async for workout in workout_repository.get_all()
    ]


@app.get('/workout/{workout_id}')
async def get_workout(
    workout_id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> Workout:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    return workout


@app.patch('/workout/{workout_id}')
async def add_set(
    set_: Set,
    workout_id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> dict[str, UUID]:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    workout.sets.append(set_)
    await workout_repository.add(workout)
    return {'id': set_.id}
