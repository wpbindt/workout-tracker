import datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from workout_tracker.api.add_set import AddSet
from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.api.models.exercise import RepUnit, DifficultyUnit
from workout_tracker.api.models.workout import Workout, Set, Reps, Difficulty
from workout_tracker.api.start_workout import StartWorkout
from workout_tracker.app import App


@pytest.mark.asyncio
async def test_that_adding_a_set_adds_a_set(fake_app: App) -> None:
    workout_id = await fake_app.execute(StartWorkout(time=datetime.datetime(1970, 1, 1, 1, 2, 3)))
    set_ = Set(
        exercise_id=uuid4(),
        intended_reps=Reps(amount=Decimal(3), unit=RepUnit.REPETITION),
        actual_reps=Reps(amount=Decimal(4), unit=RepUnit.REPETITION),
        difficulty=Difficulty(amount=Decimal(4), unit=DifficultyUnit.KILOGRAM),
    )

    await fake_app.execute(AddSet(
        workout_id=workout_id,
        set_=set_,
    ))

    returned_workout = await fake_app.execute(GetWorkout(workout_id))
    expected_workout = Workout(
        id=workout_id,
        time=datetime.datetime(1970, 1, 1, 1, 2, 3),
        sets=[set_],
    )
    assert returned_workout == expected_workout


@pytest.mark.asyncio
async def test_that_adding_multiple_sets_adds_multiple_sets(fake_app: App) -> None:
    workout_id = await fake_app.execute(StartWorkout(time=datetime.datetime(1970, 1, 1, 1, 2, 3)))
    sets = [
        Set(
            exercise_id=uuid4(),
            intended_reps=Reps(amount=Decimal(3), unit=RepUnit.REPETITION),
            actual_reps=Reps(amount=Decimal(4), unit=RepUnit.REPETITION),
            difficulty=Difficulty(amount=Decimal(4), unit=DifficultyUnit.KILOGRAM),
        ),
        Set(
            exercise_id=uuid4(),
            intended_reps=Reps(amount=Decimal(9), unit=RepUnit.SECONDS),
            actual_reps=Reps(amount=Decimal(4), unit=RepUnit.SECONDS),
            difficulty=Difficulty(amount=Decimal(7), unit=DifficultyUnit.KILOGRAM),
        ),
    ]

    for set_ in sets:
        await fake_app.execute(AddSet(
            workout_id=workout_id,
            set_=set_,
        ))

    returned_workout = await fake_app.execute(GetWorkout(workout_id))
    expected_workout = Workout(
        id=workout_id,
        time=datetime.datetime(1970, 1, 1, 1, 2, 3),
        sets=sets,
    )
    assert returned_workout == expected_workout
