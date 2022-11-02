from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from workout_tracker.repositories.factory import exercise_repository_factory, workout_repository_factory
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
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
) -> Exercise:
    workout = (await exercise_repository.get_by_ids({exercise_id}))[exercise_id]
    return workout


@api_router.post('/workout', tags=['api'])
async def create_workout(
    time: datetime | None = None,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> dict[str, UUID]:
    workout = Workout() if time is None else Workout(time=time)
    await workout_repository.add(workout)
    return {'id': workout.id}


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
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> Set:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    for set in workout.sets:
        if set.id == set_id:
            return set
    raise Exception


@api_router.patch('/workout/{workout_id}', tags=['api'])
async def add_set(
    set_: Set,
    workout_id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
) -> dict[str, UUID]:
    workout = (await workout_repository.get_by_ids({workout_id}))[workout_id]
    workout.sets.append(set_)
    await workout_repository.add(workout)
    return {'id': set_.id}