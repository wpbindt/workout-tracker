from collections import defaultdict
from decimal import Decimal
from enum import Enum
from typing import Any, Type, TypeVar

from pydantic import BaseModel

__all__ = (
    'serialize',
    'deserialize',
)


def serialize(value: Any) -> Any:
    serializers = {
        BaseModel: serialize_pydantic_model,
        dict: serialize_dict_like,
        Enum: serialize_enum,
        Decimal: float,
    }
    for type_, serializer in serializers.items():
        if isinstance(value, type_):
            return serializer(value)
    return value


def serialize_pydantic_model(value: BaseModel) -> dict[str, Any]:
    return serialize(value.dict())


def serialize_dict_like(value: dict[str, Any]) -> dict[str, Any]:
    return {
        k: serialize(v)
        for k, v in value.items()
    }


def serialize_enum(value: Enum) -> str | int:
    return value.value


T = TypeVar('T')


def deserialize_pydantic_model(value: Any, target_type: Type[T]) -> T:
    return target_type(**value)


def deserialize(value: Any, target_type: Type[T]) -> T:
    deserializers = {
        BaseModel: deserialize_pydantic_model,
    }
    for type, deserializer in deserializers.items():
        if issubclass(target_type, type):
            return deserializer(value, target_type)

    return value
