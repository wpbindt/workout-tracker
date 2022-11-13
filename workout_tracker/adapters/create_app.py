import os

from motor.motor_asyncio import AsyncIOMotorClient

from workout_tracker.adapters.repositories.mongo_repository import MongoRepository
from workout_tracker.adapters.repositories.serializers import deserialize, serialize
from workout_tracker.api.models.exercise import Exercise
from workout_tracker.api.models.workout import Workout
from workout_tracker.app import App
from workout_tracker.repositories.repository import Repositories


async def create_app():
    mongo_client = AsyncIOMotorClient(
        os.environ['MONGO_URI'],
    )
    return App(
        repositories=Repositories(
            workout=MongoRepository(
                mongo_client=mongo_client,
                database='workout_tracker',
                collection='workout',
                deserialize_entity=lambda value: deserialize(value, target_type=Workout),
                serialize_entity=serialize,
            ),
            exercise=MongoRepository(
                mongo_client=mongo_client,
                database='workout_tracker',
                collection='exercise',
                deserialize_entity=lambda value: deserialize(value, target_type=Exercise),
                serialize_entity=serialize,
            ),
        )
    )
