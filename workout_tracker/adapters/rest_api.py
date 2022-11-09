from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from workout_tracker.adapters.create_app import create_app
from workout_tracker.app import App
from workout_tracker.internal_api.add_set import AddSet
from workout_tracker.internal_api.get_exercise import GetExercise
from workout_tracker.internal_api.get_set import GetSet
from workout_tracker.internal_api.get_workout import GetWorkout
from workout_tracker.internal_api.list_exercises import ListExercises
from workout_tracker.internal_api.start_workout import StartWorkout
from workout_tracker.models.exercise import Exercise
from workout_tracker.models.workout import Workout, Set

api_router = APIRouter()


@api_router.get('/exercise', tags=['api'])
async def list_exercises(
    app: App = Depends(create_app),
) -> list[Exercise]:
    return await app.execute(ListExercises())


@api_router.get('/exercise/{exercise_id}', tags=['api'])
async def get_exercise(
    exercise_id: UUID,
    app: App = Depends(create_app),
) -> Exercise:
    return await app.execute(GetExercise(exercise_id))


@api_router.post('/workout', tags=['api'])
async def create_workout(
    time: datetime | None = None,
    app: App = Depends(create_app),
) -> dict[str, UUID]:
    workout_id = await app.execute(StartWorkout(time=time))
    return {'id': workout_id}


@api_router.get('/workout/{workout_id}', tags=['api'])
async def get_workout(
    workout_id: UUID,
    app: App = Depends(create_app)
) -> Workout:
    return await app.execute(GetWorkout(workout_id))


@api_router.get('/workout/{workout_id}/{set_id}', tags=['api'])
async def get_set(
    workout_id: UUID,
    set_id: UUID,
    app: App = Depends(create_app),
) -> Set:
    return await app.execute(GetSet(workout_id=workout_id, set_id=set_id))


@api_router.patch('/workout/{workout_id}', tags=['api'])
async def add_set(
    set_: Set,
    workout_id: UUID,
    app: App = Depends(create_app),
) -> dict[str, UUID]:
    set_id = await app.execute(AddSet(set_=set_, workout_id=workout_id))
    return {'id': set_id}
