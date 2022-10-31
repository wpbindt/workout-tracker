from abc import ABC, abstractmethod
from dbm import gnu as gnudbm
from pathlib import Path
from typing import Generic, TypeVar, AbstractSet, Mapping, Callable, Protocol, AsyncIterator

EntityId = TypeVar('EntityId', covariant=True)


class HasId(Protocol[EntityId]):
    @property
    def id(self) -> EntityId:
        ...


Entity = TypeVar('Entity', bound=HasId)


class Repository(ABC, Generic[Entity, EntityId]):
    @abstractmethod
    async def get_by_ids(
        self,
        ids: AbstractSet[EntityId],
    ) -> Mapping[EntityId, Entity]:
        ...

    @abstractmethod
    async def add(self, entity: Entity) -> None:
        ...

    @abstractmethod
    def get_all(self) -> AsyncIterator[Entity]:
        ...


class LinuxDBRepository(Repository[Entity, EntityId], Generic[Entity, EntityId]):
    def __init__(
        self,
        db_path: Path,
        entity_serializer: Callable[[Entity], str],
        entity_deserializer: Callable[[str], Entity],
    ) -> None:
        self._db_path = db_path
        self._serialize = entity_serializer
        self._deserialize = entity_deserializer

    async def get_by_ids(self, ids: AbstractSet[EntityId]) -> Mapping[EntityId, Entity]:
        with gnudbm.open(self._db_path, 'r') as db:
            return {
                id_: self._deserialize(db[str(id_)].decode())
                for id_ in ids
            }

    async def add(self, entity: Entity) -> None:
        with gnudbm.open(self._db_path, 'c') as db:
            db[str(entity.id)] = self._serialize(entity)

    async def get_all(self) -> AsyncIterator[Entity]:
        with gnudbm.open(self._db_path, 'r') as db:
            key = db.firstkey()
            while key is not None:
                value = self._deserialize(db[key].decode())
                yield value
                key = db.nextkey(key)


def create_linux_db_repository(
    db_path: Path,
    entity_serializer: Callable[[Entity], str],
    entity_deserializer: Callable[[str], Entity],
) -> Callable[[], LinuxDBRepository[Entity, EntityId]]:
    def dependency():
        with gnudbm.open(db_path, 'c'):
            pass
        return LinuxDBRepository(
            db_path,
            entity_serializer,
            entity_deserializer
        )
    return dependency
