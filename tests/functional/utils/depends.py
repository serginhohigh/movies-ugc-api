import uuid
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from utils.jwt import generate_acess_token

ACCESS_TOKEN = generate_acess_token()
ACCESS_TOKEN_INVALID = generate_acess_token(invalid=True)

MOVIE_UUID = str(uuid.uuid4())
MOVIE_UUID_INVALID = 123

USER_UUID = str(uuid.uuid4())

REVIEW_UUID = str(uuid.uuid4())

HEADER_WITH_TOKEN = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
HEADER_WITH_INDVALID_TOKEN = {'Authorization': f'Bearer {ACCESS_TOKEN_INVALID}'}


async def create_review() -> None:
    client = AsyncIOMotorClient(
        settings.mongo_database_uri, uuidRepresentation='standard'
    )
    db = client['ugc']
    collection = db['reviews']

    await collection.insert_one(
        {
            '_id': uuid.UUID(REVIEW_UUID),
            'movie_id': uuid.UUID(MOVIE_UUID),
            'user_id': uuid.UUID(USER_UUID),
            'text': 'BEST_MOVIE_IN_THE_WORLD',
            'likes': [],
            'dislikes': [],
            'created_at': datetime.now(timezone.utc),
        }
    )
