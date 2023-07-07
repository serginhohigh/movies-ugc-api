from exceptions.base import AlreadyExistsError, NotFoundError


class RatingNotFoundError(NotFoundError):
    entity_name: str = 'Rating'


class RatingAlreadyExistsError(AlreadyExistsError):
    entity_name: str = 'Rating'
