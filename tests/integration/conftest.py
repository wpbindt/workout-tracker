from tests.integration.fixtures.repository import repository
from tests.integration.fixtures.mongo_repository import mongo_repository
from tests.integration.fixtures.fake_repository import fake_repository
from tests.integration.fixtures.linux_db_repository import linux_db_repository

__all__ = (
    repository,
    linux_db_repository,
    fake_repository,
    mongo_repository,
)
