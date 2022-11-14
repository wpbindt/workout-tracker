import datetime

import pytest

from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.api.models.workout import Workout
from workout_tracker.api.start_workout import StartWorkout
from workout_tracker.app import App


@pytest.mark.asyncio
async def test_that_get_workout_retrieves_started_workout(fake_app: App) -> None:
    workout_id = await fake_app.execute(StartWorkout(time=datetime.datetime(1970, 1, 1, 1, 2, 3)))

    returned_workout = await fake_app.execute(GetWorkout(workout_id))

    expected_workout = Workout(
        id=workout_id,
        time=datetime.datetime(1970, 1, 1, 1, 2, 3),
        sets=[]
    )
    assert returned_workout == expected_workout
