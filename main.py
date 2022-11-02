import json
from datetime import datetime
from pathlib import Path
from typing import Callable
from uuid import UUID

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from models.exercise import Exercise
from models.workout import Workout, Set
from repositories.repository import create_linux_db_repository, Repository

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


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


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request},
    )


@app.get('/workout', response_class=HTMLResponse)
async def individual_workout(
    request: Request,
    id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
):
    workout = (await workout_repository.get_by_ids({id}))[id]
    exercises = {exercise.id: exercise async for exercise in exercise_repository.get_all()}
    return templates.TemplateResponse(
        'workout.html',
        {
            'request': request,
            'available_exercises': exercises,
            'workout': workout
        }
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


@app.get('/workouts')
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


@app.get('/workout/{workout_id}/{set_id}')
async def get_set(
    workout_id: UUID,
    set_id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> Set:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    for set in workout.sets:
        if set.id == set_id:
            return set
    raise Exception


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
