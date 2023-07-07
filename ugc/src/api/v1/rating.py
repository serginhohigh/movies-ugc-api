from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status

from api.v1.utils.validators import AccessToken, valid_access_token
from core.containers import Container
from exceptions.base import AlreadyExistsError, NotFoundError
from models.base import Message
from models.movies import MovieRate, MovieRatingResponse
from models.ratings import RatingResponse
from services.ratings import RatingsService

router = APIRouter()


@router.get(
    '',
    response_model=MovieRatingResponse,
    summary='Получить рейтинг кинопроизведения',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_404_NOT_FOUND: {'model': Message},
        status.HTTP_409_CONFLICT: {'model': Message},
    },
)
@inject
async def get_bookmarks(
    movie_id: UUID,
    ratings_service: RatingsService = Depends(
        Provide[Container.ratings_service],
    ),
) -> MovieRatingResponse:
    """
    Получить общий рейтинг кинопроизведения.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.

    - **movie_id**: сортировка по дате добавления
    """

    try:
        rating = await ratings_service.get_movie_rating(movie_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie not found',
        ) from None

    try:
        return MovieRatingResponse(movie_id=rating.id_, rating=rating.get_rating())
    except ZeroDivisionError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Something went wrong when calculate rating',
        ) from None


@router.put(
    '',
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Оценить кинопроизведение',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_409_CONFLICT: {'model': Message},
    },
)
@inject
async def rate_movie(
    movie: MovieRate,
    access_token: AccessToken = Depends(valid_access_token),
    ratings_service: RatingsService = Depends(
        Provide[Container.ratings_service],
    ),
) -> RatingResponse:
    """
    Оценить кинопроизведение по 10 бальной шкале.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.
    """

    user_id = access_token.sub
    movie_id = movie.id
    movie_rating = movie.rating

    try:
        rating = await ratings_service.create_movie_rating(
            user_id,
            movie_id,
            movie_rating,
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Rating already exists',
        ) from None

    return RatingResponse(
        id=rating.id_,
        user_id=rating.user_id,
        movie_id=rating.movie_id,
        rating=rating.rating,
        created_at=rating.created_at,
    )


@router.delete(
    '',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить оценку кинопроизведения',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_404_NOT_FOUND: {'model': Message},
    },
)
@inject
async def delete_rating(
    movie_id: UUID = Body(..., embed=True),
    access_token: AccessToken = Depends(valid_access_token),
    ratings_service: RatingsService = Depends(
        Provide[Container.ratings_service],
    ),
) -> None:
    """
    Удалить оценку кинопроизведения.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.
    """

    user_id = access_token.sub
    movie_id = movie_id

    try:
        await ratings_service.delete_movie_rating(user_id, movie_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Rating or movie not found',
        ) from None
