from uuid import UUID

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError

from db.mongo import MongoSearcher
from exceptions.reviews import (
    ReviewAlreadyExistsError,
    ReviewNotFoundError,
    ReviewNotModifiedError,
)
from models.reviews import Review
from repositories.abstract.repository import AbstractRepository


class ReviewsRepository(AbstractRepository):
    def __init__(
        self,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
        database: str,
        collection: str,
    ) -> None:
        self.db = mongo_client[database]
        self.collection = self.db[collection]

    async def get_by_movie_id(
        self, movie_id: UUID, searcher: MongoSearcher
    ) -> list[Review]:
        project = {
            '_id': 1,
            'user_id': 1,
            'movie_id': 1,
            'text': 1,
            'likes': {'$size': '$likes'},
            'dislikes': {'$size': '$dislikes'},
            'created_at': 1,
        }

        cursor = self.collection.find({'movie_id': {'$eq': movie_id}}, project)
        cursor.sort(searcher.key, searcher.order).limit(searcher.limit).skip(
            searcher.skip
        )

        return [Review(**review) for review in await cursor.to_list(None)]

    async def rate_by_id(
        self, review_id: UUID, user_id: UUID, operator: str, field: str
    ) -> None:
        result = await self.collection.update_one(
            {'_id': review_id}, {operator: {field: user_id}}
        )

        if not result.matched_count:
            msg = f'review({review_id})'
            raise ReviewNotFoundError(msg) from None

        if not result.modified_count:
            msg = (
                f'Review({review_id}, user({user_id}), '
                f'operator({operator}), field({field}))'
            )
            raise ReviewNotModifiedError(msg) from None

    async def add(self, user_id: UUID, movie_id: UUID, review_text: str) -> Review:
        review = Review(user_id=user_id, movie_id=movie_id, text=review_text)

        try:
            await self.collection.insert_one(review.dict(by_alias=True))
        except DuplicateKeyError:
            msg = f'{review}'
            raise ReviewAlreadyExistsError(msg) from None

        return review

    async def delete(self, user_id: UUID, movie_id: UUID) -> None:
        result = await self.collection.delete_one(
            {'user_id': user_id, 'movie_id': movie_id}
        )

        if not result.deleted_count:
            msg = f'Review(user({user_id}), movie({movie_id})'
            raise ReviewNotFoundError(msg) from None
