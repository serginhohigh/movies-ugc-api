import uuid
from datetime import datetime, timezone

from pydantic import Field

from models.base import BaseModel


class Rating(BaseModel):
    id_: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: uuid.UUID
    movie_id: uuid.UUID
    rating: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        return (
            f'Rating(user({self.user_id}), '
            f'movie({self.movie_id}), rating({self.rating}))'
        )


class RatingResponse(Rating):
    id_: uuid.UUID = Field(alias='id')
