from exceptions.base import NotFoundError


class MovieNotFoundError(NotFoundError):
    entity_name: str = 'Movie'
