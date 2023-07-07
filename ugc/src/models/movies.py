from uuid import UUID

from pydantic import Field

from models.base import BaseModel


class MovieReview(BaseModel):
    movie_id: UUID
    text: str


class MovieRate(BaseModel):
    movie_id: UUID
    rating: int = Field(gt=1, lt=11)

    @property
    def id(self) -> UUID:
        return self.movie_id


class MovieRating(BaseModel):
    id_: UUID = Field(alias='_id')
    rate_count: int
    rate_value: int

    def get_rating(self) -> float:
        return round(self.rate_value / self.rate_count, 1)


class MovieRatingResponse(BaseModel):
    movie_id: UUID
    rating: float
