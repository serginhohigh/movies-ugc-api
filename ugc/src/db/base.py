from typing import NamedTuple


class Searcher(NamedTuple):
    sort_field: str
    page_size: int
    page_number: int
