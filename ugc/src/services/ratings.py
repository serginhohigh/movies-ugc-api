from uuid import UUID

from models.movies import MovieRating
from models.ratings import Rating
from repositories.ratings import RatingsRepository


class RatingsService:
    def __init__(
        self,
        ratings_repository: RatingsRepository,
    ) -> None:
        self._repository = ratings_repository

    async def get_movie_rating(self, movie_id: UUID) -> MovieRating:
        return await self._repository.get_movie_by_id(movie_id)

    async def create_movie_rating(
        self,
        user_id: UUID,
        movie_id: UUID,
        rating: int,
    ) -> Rating:
        return await self._repository.add(user_id, movie_id, rating)

    async def delete_movie_rating(self, user_id: UUID, movie_id: UUID) -> None:
        await self._repository.delete(user_id, movie_id)
