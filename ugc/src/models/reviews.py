import enum
import uuid
from datetime import datetime, timezone

from pydantic import Field

from models.movies import MovieReview


class Review(MovieReview):
    id_: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: uuid.UUID
    likes: int | list = Field(default_factory=list)
    dislikes: int | list = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        return (
            f'Review(user({self.user_id}), '
            f'movie({self.movie_id}), text({self.text[:10]}))'
        )


class ReviewResponse(Review):
    pass


class ReviewRate(enum.Enum):
    def __str__(self) -> str:
        return self.value


class ReviewRateAction(ReviewRate):
    ADD = '$addToSet'
    DELETE = '$pull'


class ReviewRateType(ReviewRate):
    LIKE = 'likes'
    DISLIKE = 'dislikes'
