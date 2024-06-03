from abc import ABC, abstractmethod
from typing import Any, Sequence

from pydantic import BaseModel


class BaseSerializer[T: Any, V: BaseModel](ABC):
    @abstractmethod
    def serialize(self, data: T) -> V:
        raise NotImplementedError


class BaseListSerializer[T: Sequence[Any], V: list[BaseModel]](ABC):
    @abstractmethod
    def serialize_list(self, data: Sequence[T]) -> list[V]:
        raise NotImplementedError
