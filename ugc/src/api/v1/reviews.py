from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from api.v1.commons.params import PageQueryParams, ReviewsSortQueryParams
from api.v1.utils.validators import AccessToken, valid_access_token
from core.containers import Container
from exceptions.base import AlreadyExistsError, NotFoundError, NotModifiedError
from models.base import Message
from models.movies import MovieReview
from models.reviews import ReviewResponse
from services.reviews import ReviewsService

router = APIRouter()


@router.get(
    '',
    response_model=list[ReviewResponse],
    summary='Получить список рецензий',
    responses={status.HTTP_403_FORBIDDEN: {'model': Message}},
)
@inject
async def get_reviews(
    movie_id: UUID,
    sort_params: ReviewsSortQueryParams = Depends(),
    page_params: PageQueryParams = Depends(),
    reviews_service: ReviewsService = Depends(
        Provide[Container.reviews_service],
    ),
) -> list[ReviewResponse]:
    """
    Список рецензий с пагинацией и сортировкой по дате, лайкам и дизлайкам.

    - **sort**: сортировка по дате создания или количеству лайков/дизлайков
    - **page[size]**: размер страницы
    - **page[number]**: номер страницы
    """

    reviews = await reviews_service.get_reviews_by_movie_id(
        movie_id,
        sort_params,
        page_params,
    )
    return [ReviewResponse(**review.dict()) for review in reviews]


@router.post(
    '',
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создать рецензию',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_409_CONFLICT: {'model': Message},
    },
)
@inject
async def create_review(
    movie_review: MovieReview,
    access_token: AccessToken = Depends(valid_access_token),
    reviews_service: ReviewsService = Depends(
        Provide[Container.reviews_service],
    ),
) -> ReviewResponse:
    """
    Cоздать рецензию.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.
    """

    user_id = access_token.sub
    movie_id = movie_review.movie_id
    review_text = movie_review.text

    try:
        review = await reviews_service.create_review(user_id, movie_id, review_text)
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Review already exists',
        ) from None
    return ReviewResponse(**review.dict(exclude={'likes', 'dislikes'}))


@router.delete(
    '',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить рецензию',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_404_NOT_FOUND: {'model': Message},
    },
)
@inject
async def delete_review(
    movie_id: UUID = Body(..., embed=True),
    access_token: AccessToken = Depends(valid_access_token),
    reviews_service: ReviewsService = Depends(
        Provide[Container.reviews_service],
    ),
) -> None:
    """
    Удалить рецензию.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.
    """

    user_id = access_token.sub

    try:
        await reviews_service.delete_review(user_id, movie_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found',
        ) from None


@router.patch(
    '',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Поставить/убрать лайк или дизлайк рецензии',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_404_NOT_FOUND: {'model': Message},
        status.HTTP_409_CONFLICT: {'model': Message},
    },
)
@inject
async def rate_review(
    review_id: UUID = Body(..., embed=True),
    action: str = Query(regex='[add|delete]'),
    type: str = Query(regex='[like|dislike]'),
    access_token: AccessToken = Depends(valid_access_token),
    reviews_service: ReviewsService = Depends(
        Provide[Container.reviews_service],
    ),
) -> None:
    """
    Оценить рецензию.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.
    """

    user_id = access_token.sub

    try:
        await reviews_service.rate_review_by_id(review_id, user_id, action, type)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found',
        ) from None
    except NotModifiedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Review not modified',
        ) from None
