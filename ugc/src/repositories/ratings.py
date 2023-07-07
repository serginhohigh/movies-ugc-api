from uuid import UUID

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError
from pymongo.results import UpdateResult

from exceptions.movies import MovieNotFoundError
from exceptions.ratings import RatingAlreadyExistsError, RatingNotFoundError
from models.movies import MovieRating
from models.ratings import Rating
from repositories.abstract.repository import AbstractRepository


class RatingsRepository(AbstractRepository):
    def __init__(
        self,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
        database: str,
        ratings_collection: str,
        movies_collection: str,
    ) -> None:
        self.db = mongo_client[database]
        self.ratings_collection = self.db[ratings_collection]
        self.movies_collection = self.db[movies_collection]

    async def get_movie_by_id(self, movie_id: UUID) -> MovieRating:
        movie = await self.movies_collection.find_one({'_id': movie_id})

        if not movie:
            msg = f'Movie({movie_id})'
            raise MovieNotFoundError(msg) from None

        return MovieRating(**movie)

    async def add(self, user_id: UUID, movie_id: UUID, user_rating: int) -> Rating:
        rating = Rating(user_id=user_id, movie_id=movie_id, rating=user_rating)

        try:
            await self.ratings_collection.insert_one(rating.dict(by_alias=True))
        except DuplicateKeyError:
            msg = f'{rating}'
            raise RatingAlreadyExistsError(msg) from None

        movie_increment_result = await self._increment_movie_rating(
            movie_id, 1, user_rating
        )
        if not movie_increment_result.matched_count:
            await self._add_movie(movie_id, 1, user_rating)

        return rating

    async def _add_movie(
        self, movie_id: UUID, rate_count: int, user_rating: int
    ) -> None:
        await self.movies_collection.insert_one(
            {'_id': movie_id, 'rate_count': rate_count, 'rate_value': user_rating}
        )

    async def _increment_movie_rating(
        self, movie_id: UUID, rate_count: int, user_rating: int
    ) -> UpdateResult:
        return await self.movies_collection.update_one(
            {'_id': movie_id},
            {'$inc': {'rate_count': rate_count, 'rate_value': user_rating}},
        )

    async def delete(self, user_id: UUID, movie_id: UUID) -> None:
        rating = await self.ratings_collection.find_one_and_delete(
            {'user_id': user_id, 'movie_id': movie_id}
        )

        if not rating:
            msg = f'Rating(user({user_id}), movie({movie_id})'
            raise RatingNotFoundError(msg) from None

        movie_increment_result = await self._increment_movie_rating(
            movie_id, -1, -rating['rating']
        )

        if not movie_increment_result.matched_count:
            msg = f'Movie({movie_id})'
            raise MovieNotFoundError(msg) from None
