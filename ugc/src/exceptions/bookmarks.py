from exceptions.base import AlreadyExistsError, NotFoundError


class BookmarkNotFoundError(NotFoundError):
    entity_name: str = 'Bookmark'


class BookmarkAlreadyExistsError(AlreadyExistsError):
    entity_name: str = 'Bookmark'
