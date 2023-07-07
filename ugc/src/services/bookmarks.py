from collections.abc import Callable
from uuid import UUID

from api.v1.commons.params import PageQueryParams, SortQueryParams
from db.mongo import MongoSearcher
from models.bookmarks import Bookmark
from repositories.bookmarks import BookmarksRepository


class BookmarksService:
    def __init__(
        self,
        bookmarks_repository: BookmarksRepository,
        searcher: Callable[..., MongoSearcher],
    ) -> None:
        self._repository = bookmarks_repository
        self.searcher = searcher

    async def get_bookmarks(
        self,
        user_id: UUID,
        sort_params: SortQueryParams,
        page_params: PageQueryParams,
    ) -> list | list[Bookmark]:
        searcher = self.searcher(
            sort_field=sort_params.sort_field,
            page_size=page_params.page_size,
            page_number=page_params.page_number,
        )
        return await self._repository.get_all(user_id, searcher)

    async def create_bookmark(self, user_id: UUID, movie_id: UUID) -> Bookmark:
        return await self._repository.add(user_id, movie_id)

    async def delete_bookmark(self, user_id: UUID, movie_id: UUID) -> None:
        await self._repository.delete(user_id, movie_id)
