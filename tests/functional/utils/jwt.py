import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt

from config import settings


def generate_acess_token(*, invalid: bool = False):
    secret_key = settings.jwt_secret_key if not invalid else '123123h1h23k12hfh'
    token_data = {
        'sub': str(uuid.uuid4()),
        'role': 'Admin',
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'type': 'access',
    }
    return jwt.encode(token_data, secret_key, settings.jwt_algorithms)
