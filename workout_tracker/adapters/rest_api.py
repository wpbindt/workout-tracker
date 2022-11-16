from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from workout_tracker.adapters.create_app import create_app
from workout_tracker.api.add_exercise import AddExercise
from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.models.workout import Workout, Set
from workout_tracker.app import App
from workout_tracker.api.add_set import AddSet
from workout_tracker.api.get_exercise import GetExercise
from workout_tracker.api.get_set import GetSet
from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.api.list_exercises import ListExercises
from workout_tracker.api.start_workout import StartWorkout

api_router = APIRouter()


@api_router.get('/exercise', tags=['api'])
async def list_exercises(
    app: App = Depends(create_app),
) -> list[Exercise]:
    return list((await ListExercises().execute(app)).values())


@api_router.get('/exercise/{exercise_id}', tags=['api'])
async def get_exercise(
    exercise_id: UUID,
    app: App = Depends(create_app),
) -> Exercise:
    return await GetExercise(exercise_id).execute(app)


@api_router.post('/workout', tags=['api'])
async def create_workout(
    time: datetime | None = None,
    app: App = Depends(create_app),
) -> dict[str, UUID]:
    workout_id = await StartWorkout(time=time).execute(app)
    return {'id': workout_id}


@api_router.get('/workout/{workout_id}', tags=['api'])
async def get_workout(
    workout_id: UUID,
    app: App = Depends(create_app)
) -> Workout:
    return await GetWorkout(workout_id).execute(app)


@api_router.get('/workout/{workout_id}/{set_id}', tags=['api'])
async def get_set(
    workout_id: UUID,
    set_id: UUID,
    app: App = Depends(create_app),
) -> Set:
    return await GetSet(workout_id=workout_id, set_id=set_id).execute(app)


@api_router.patch('/workout/{workout_id}', tags=['api'])
async def add_set(
    set_: Set,
    workout_id: UUID,
    app: App = Depends(create_app),
) -> dict[str, UUID]:
    set_id = await AddSet(set_=set_, workout_id=workout_id).execute(app)
    return {'id': set_id}


@api_router.post('/exercise', tags=['api'])
async def add_exercise(
    exercise: Exercise,
    app: App = Depends(create_app),
) -> dict[str, UUID]:
    exercise_id = await AddExercise(exercise).execute(app)
    return {'id': exercise_id}
