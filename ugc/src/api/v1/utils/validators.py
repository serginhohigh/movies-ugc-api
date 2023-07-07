from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError, validator

from core.containers import Container

bearer_in_headers = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid access token',
)


class AccessToken(BaseModel):
    sub: UUID
    role: str
    exp: int
    iat: int
    type: str

    @validator('type')
    def type_should_be_access(cls, v: str) -> str:  # noqa: N805
        if v != 'access':
            raise ValueError
        return v


@inject
async def valid_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_in_headers),
    jwt_secret_key: str = Depends(Provide[Container.config.jwt_secret_key]),
    jwt_algorithms: str = Depends(Provide[Container.config.jwt_algorithms]),
) -> AccessToken:
    """Проверка валидности JWT access token'a."""

    access_token = credentials.credentials

    try:
        payload = jwt.decode(
            access_token,
            jwt_secret_key,
            algorithms=jwt_algorithms.split(','),
        )
        payload = AccessToken(**payload)  # type: ignore
    except JWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception

    return payload  # type: ignore
