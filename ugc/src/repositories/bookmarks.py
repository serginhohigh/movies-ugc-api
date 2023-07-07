from uuid import UUID

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError

from db.mongo import MongoSearcher
from exceptions.bookmarks import BookmarkAlreadyExistsError, BookmarkNotFoundError
from models.bookmarks import Bookmark
from repositories.abstract.repository import AbstractRepository


class BookmarksRepository(AbstractRepository):
    def __init__(
        self,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
        database: str,
        collection: str,
    ) -> None:
        self.db = mongo_client[database]
        self.collection = self.db[collection]

    async def get_all(
        self,
        user_id: UUID,
        searcher: MongoSearcher,
    ) -> list | list[Bookmark]:
        cursor = self.collection.find({'user_id': user_id})
        cursor.sort(searcher.key, searcher.order).limit(searcher.limit).skip(
            searcher.skip
        )

        return [Bookmark(**bookmark) for bookmark in await cursor.to_list(None)]

    async def add(self, user_id: UUID, movie_id: UUID) -> Bookmark:
        bookmark = Bookmark(user_id=user_id, movie_id=movie_id)

        try:
            await self.collection.insert_one(bookmark.dict(by_alias=True))
        except DuplicateKeyError:
            msg = f'{bookmark}'
            raise BookmarkAlreadyExistsError(msg) from None

        return bookmark

    async def delete(self, user_id: UUID, movie_id: UUID) -> None:
        bookmark = Bookmark(user_id=user_id, movie_id=movie_id)

        result = await self.collection.delete_one(
            bookmark.dict(include={'user_id', 'movie_id'})
        )
        if not result.deleted_count:
            msg = f'{bookmark}'
            raise BookmarkNotFoundError(msg) from None
