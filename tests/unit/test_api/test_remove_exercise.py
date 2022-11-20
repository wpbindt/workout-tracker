import pytest

from workout_tracker.api.add_exercise import AddExercise
from workout_tracker.api.list_exercises import ListExercises
from workout_tracker.api.models.exercise import Exercise, DifficultyUnit, RepUnit
from workout_tracker.api.remove_exercise import RemoveExercise
from workout_tracker.app import App


@pytest.mark.asyncio
async def test_list_exercises_returns_added_exercise(fake_app: App) -> None:
    exercise = Exercise(
        name='bench press',
        description='lay down on bench and press',
        difficulty_unit=DifficultyUnit.KILOGRAM,
        rep_unit=RepUnit.REPETITION,
    )
    await fake_app.execute(AddExercise(exercise))

    await fake_app.execute(RemoveExercise(exercise.id))

    returned_exercises = await fake_app.execute(ListExercises())
    assert returned_exercises == {}
