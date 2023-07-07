from abc import ABC, abstractmethod
from typing import Any as AnyType


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, *args, **kwargs) -> AnyType:
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs) -> AnyType:
        pass
