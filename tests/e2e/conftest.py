import os

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


@pytest_asyncio.fixture
async def fixture_server() -> str:
    yield 'http://workout_tracker:8001'

    mongo_client = AsyncIOMotorClient(os.environ['MONGO_CONNECTION_URI'])
    db = mongo_client['workout_tracker']
    await db.exercise.drop()
    await db.workout.drop()
