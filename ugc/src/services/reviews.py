from collections.abc import Callable
from uuid import UUID

from api.v1.commons.params import PageQueryParams, ReviewsSortQueryParams
from db.mongo import MongoSearcher
from models.reviews import Review, ReviewRateAction, ReviewRateType
from repositories.reviews import ReviewsRepository


class ReviewsService:
    def __init__(
        self,
        reviews_repository: ReviewsRepository,
        searcher: Callable[..., MongoSearcher],
    ) -> None:
        self._repository = reviews_repository
        self.searcher = searcher

    async def get_reviews_by_movie_id(
        self,
        movie_id: UUID,
        sort_params: ReviewsSortQueryParams,
        page_params: PageQueryParams,
    ) -> list | list[Review]:
        searcher = self.searcher(
            sort_field=sort_params.sort_field,
            page_size=page_params.page_size,
            page_number=page_params.page_number,
        )
        return await self._repository.get_by_movie_id(movie_id, searcher)

    async def rate_review_by_id(
        self, review_id: UUID, user_id: UUID, action: str, type: str
    ) -> None:
        operator = str(ReviewRateAction[action.upper()])
        field = str(ReviewRateType[type.upper()])
        return await self._repository.rate_by_id(review_id, user_id, operator, field)

    async def create_review(
        self, user_id: UUID, movie_id: UUID, review_text: str
    ) -> Review:
        return await self._repository.add(user_id, movie_id, review_text)

    async def delete_review(self, user_id: UUID, movie_id: UUID) -> None:
        await self._repository.delete(user_id, movie_id)
