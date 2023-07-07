from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status

from api.v1.commons.params import PageQueryParams, SortQueryParams
from api.v1.utils.validators import AccessToken, valid_access_token
from core.containers import Container
from exceptions.base import AlreadyExistsError, NotFoundError
from models.base import Message
from models.bookmarks import BookmarkResponse
from services.bookmarks import BookmarksService

router = APIRouter()


@router.get(
    '',
    response_model=list[BookmarkResponse],
    summary='Получить список закладок',
    responses={status.HTTP_403_FORBIDDEN: {'model': Message}},
)
@inject
async def get_bookmarks(
    sort_params: SortQueryParams = Depends(),
    page_params: PageQueryParams = Depends(),
    access_token: AccessToken = Depends(valid_access_token),
    bookmarks_service: BookmarksService = Depends(
        Provide[Container.bookmarks_service],
    ),
) -> list[BookmarkResponse]:
    """
    Список закладок с пагинацией.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.

    - **sort**: сортировка по дате добавления
    - **page[size]**: размер страницы
    - **page[number]**: номер страницы
    """

    user_id = access_token.sub

    bookmarks = await bookmarks_service.get_bookmarks(
        user_id,
        sort_params,
        page_params,
    )
    return [
        BookmarkResponse(user_id=bookmark.user_id, movie_id=bookmark.movie_id)
        for bookmark in bookmarks
    ]


@router.post(
    '',
    response_model=BookmarkResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Добавить закладку',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_409_CONFLICT: {'model': Message},
    },
)
@inject
async def create_bookmark(
    movie_id: UUID = Body(..., embed=True),
    access_token: AccessToken = Depends(valid_access_token),
    bookmarks_service: BookmarksService = Depends(
        Provide[Container.bookmarks_service],
    ),
) -> BookmarkResponse:
    """
    Добавить кинопроизведение в закладки.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.


    - **movie_id**: ID кинопроизведения
    """

    user_id = access_token.sub

    try:
        result = await bookmarks_service.create_bookmark(user_id, movie_id)
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Bookmark already exists',
        ) from None
    return BookmarkResponse(user_id=result.user_id, movie_id=result.user_id)


@router.delete(
    '',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить закладку',
    responses={
        status.HTTP_403_FORBIDDEN: {'model': Message},
        status.HTTP_404_NOT_FOUND: {'model': Message},
    },
)
@inject
async def delete_bookmark(
    movie_id: UUID = Body(..., embed=True),
    access_token: AccessToken = Depends(valid_access_token),
    bookmarks_service: BookmarksService = Depends(
        Provide[Container.bookmarks_service],
    ),
) -> None:
    """
    Удалить кинопроизведение из закладок.

    Для успешного выполнения запроса необходимо добавить хедер
    следующего формата: `Authorization: Bearer JWT`.

    Информацию по получению указанного выше токена смотрите в сервисе **AUTH**.

    - **movie_id**: ID кинопроизведения
    """

    user_id = access_token.sub

    try:
        await bookmarks_service.delete_bookmark(user_id, movie_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bookmark not found',
        ) from None
