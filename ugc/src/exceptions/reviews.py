from exceptions.base import AlreadyExistsError, NotFoundError, NotModifiedError


class ReviewNotFoundError(NotFoundError):
    entity_name: str = 'Review'


class ReviewAlreadyExistsError(AlreadyExistsError):
    entity_name: str = 'Review'


class ReviewNotModifiedError(NotModifiedError):
    entity_name: str = 'Review'
