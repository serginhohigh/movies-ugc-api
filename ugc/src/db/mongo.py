from collections.abc import Generator

import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING

from db.base import Searcher


class MongoSearcher(Searcher):
    @property
    def key(self) -> str:
        return self.sort_field.lstrip('-')

    @property
    def order(self) -> int:
        return DESCENDING if self.sort_field.startswith('-') else ASCENDING

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def skip(self) -> int:
        return self.page_size * self.page_number - self.page_size


def init_mongo(
    uri: str,
) -> Generator[motor.motor_asyncio.AsyncIOMotorClient, None, None]:
    session = motor.motor_asyncio.AsyncIOMotorClient(uri, uuidRepresentation='standard')
    yield session
    session.close()
