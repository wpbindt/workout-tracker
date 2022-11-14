import pytest

from tests.integration.fixtures.fake_repository import FakeRepository
from workout_tracker.app import App
from workout_tracker.repositories.repository import Repositories


@pytest.fixture
def fake_repositories() -> Repositories:
    return Repositories(
        workout=FakeRepository(),
        exercise = FakeRepository()
    )


@pytest.fixture
def fake_app(fake_repositories: Repositories) -> App:
    return App(fake_repositories)
