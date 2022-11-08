from workout_tracker.adapters.repository_factory import workout_repository_factory, exercise_repository_factory
from workout_tracker.app import App
from workout_tracker.repositories.repository import Repositories


async def create_app():
    return App(
        repositories=Repositories(
            workout=workout_repository_factory(),
            exercise=exercise_repository_factory()
        )
    )
