from __future__ import annotations

from collections import Counter
from uuid import uuid4, UUID

import pytest

from tests.integration.fixtures.test_object import FixtureObject
from workout_tracker.repositories.repository import Repository


@pytest.mark.asyncio
async def test_that_repository_does_not_return_unsaved_data(repository: Repository[FixtureObject, UUID]) -> None:
    entity_id = uuid4()
    retrieved_entities = await repository.get_by_ids({entity_id})

    assert retrieved_entities == {}


@pytest.mark.asyncio
async def test_that_repository_is_able_to_retrieve_saved_data(repository: Repository[FixtureObject, UUID]) -> None:
    entity_id = uuid4()
    entity = FixtureObject(id=entity_id, value='hi', other_value=99)
    await repository.add(entity)
    retrieved_entity = (await repository.get_by_ids({entity_id}))[entity_id]

    assert entity == retrieved_entity


@pytest.mark.asyncio
async def test_that_repository_is_able_to_retrieve_multiple_saved_data(
    repository: Repository[FixtureObject, UUID],
) -> None:
    entity_id_1 = uuid4()
    entity_1 = FixtureObject(id=entity_id_1, value='hi', other_value=99)
    entity_id_2 = uuid4()
    entity_2 = FixtureObject(id=entity_id_2, value='mom', other_value=66)

    await repository.add(entity_1)
    await repository.add(entity_2)
    retrieved_entities = await repository.get_by_ids({entity_id_1, entity_id_2})

    assert retrieved_entities == {entity_id_1: entity_1, entity_id_2: entity_2}


@pytest.mark.asyncio
async def test_that_repository_can_loop_through_data(repository: Repository[FixtureObject, UUID]) -> None:
    entities = {
        FixtureObject(id=uuid4(), value='hi', other_value=99),
        FixtureObject(id=uuid4(), value='mom', other_value=66),
    }

    for entity in entities:
        await repository.add(entity)
    retrieved_entities = [d async for d in repository.get_all()]

    assert Counter(retrieved_entities) == Counter(entities)


@pytest.mark.asyncio
async def test_that_repository_only_returns_that_which_is_asked_for(
    repository: Repository[FixtureObject, UUID],
) -> None:
    entity_id_1 = uuid4()
    entity_1 = FixtureObject(id=entity_id_1, value='hi', other_value=99)
    entity_id_2 = uuid4()
    entity_2 = FixtureObject(id=entity_id_2, value='mom', other_value=66)

    await repository.add(entity_1)
    await repository.add(entity_2)
    retrieved_entities = await repository.get_by_ids({entity_id_1})

    assert retrieved_entities == {entity_id_1: entity_1}


@pytest.mark.asyncio
async def test_that_repository_is_able_to_update_data(repository: Repository[FixtureObject, UUID]) -> None:
    entity_id = uuid4()
    entity = FixtureObject(id=entity_id, value='hi', other_value=99)
    await repository.add(entity)
    mutated_entity = FixtureObject(id=entity_id, value='mom', other_value=99)
    await repository.add(mutated_entity)

    retrieved_entity = (await repository.get_by_ids({entity_id}))[entity_id]

    assert mutated_entity == retrieved_entity


@pytest.mark.asyncio
async def test_that_repository_is_able_to_remove_data(repository: Repository[FixtureObject, UUID]) -> None:
    entity_id = uuid4()
    entity = FixtureObject(id=entity_id, value='hi', other_value=99)
    await repository.add(entity)

    await repository.remove(entity_id)

    retrieved_entities = await repository.get_by_ids({entity_id})
    assert retrieved_entities == {}
