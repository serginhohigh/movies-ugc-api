import uuid
from datetime import datetime, timezone

from pydantic import Field

from models.base import BaseModel


class Bookmark(BaseModel):
    id_: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: uuid.UUID
    movie_id: uuid.UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        return f'Bookmark(User({self.user_id}), Movie({self.movie_id}))'


class BookmarkResponse(BaseModel):
    user_id: uuid.UUID
    movie_id: uuid.UUID
