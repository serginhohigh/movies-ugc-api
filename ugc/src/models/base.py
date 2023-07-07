from collections.abc import Callable
from typing import Any as AnyType

import orjson
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(
    v: AnyType,  # noqa: ANN401
    *,
    default: Callable[[AnyType], AnyType] | None,
) -> str:
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Message(BaseModel):
    detail: str
