from fastapi import Query


class PageQueryParams:
    def __init__(
        self,
        page_size: int = Query(default=25, gt=0, lt=50, alias='page[size]'),
        page_number: int = Query(default=1, gt=0, alias='page[number]'),
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number


class SortQueryParams:
    def __init__(
        self,
        sort_field: str = Query(
            default='-created_at',
            regex='^(-?)created_at',
            alias='sort',
        ),
    ) -> None:
        self.sort_field = sort_field


class ReviewsSortQueryParams:
    def __init__(
        self,
        sort_field: str = Query(
            default='-created_at',
            alias='sort',
        ),
    ) -> None:
        self.sort_field = sort_field
