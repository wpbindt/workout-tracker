from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from workout_tracker.adapters.create_app import create_app
from workout_tracker.adapters.repository_factory import exercise_repository_factory, workout_repository_factory
from workout_tracker.app import App
from workout_tracker.internal_api.add_set import AddSet
from workout_tracker.internal_api.get_exercise import GetExercise
from workout_tracker.internal_api.get_set import GetSet
from workout_tracker.internal_api.start_workout import StartWorkout
from workout_tracker.models.exercise import Exercise
from workout_tracker.models.workout import Workout, Set
from workout_tracker.repositories.repository import Repository

api_router = APIRouter()


@api_router.post('/exercise', tags=['api'])
async def create_exercise(
    exercise: Exercise,
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> dict[str, UUID]:
    await exercise_repository.add(exercise)
    return {'id': exercise.id}


@api_router.get('/exercise', tags=['api'])
async def list_exercises(
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> list[Exercise]:
    return [
        exercise
        async for exercise in exercise_repository.get_all()
    ]


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


@api_router.get('/workouts', tags=['api'])
async def list_workouts(
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> list[Workout]:
    return [
        workout
        async for workout in workout_repository.get_all()
    ]


@api_router.get('/workout/{workout_id}', tags=['api'])
async def get_workout(
    workout_id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> Workout:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    return workout


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
