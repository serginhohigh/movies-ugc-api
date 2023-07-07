from http import HTTPStatus

import pytest

from utils.depends import (
    HEADER_WITH_INDVALID_TOKEN,
    HEADER_WITH_TOKEN,
    MOVIE_UUID,
    MOVIE_UUID_INVALID,
)

BOOKMARKS_URL_PATH = '/bookmarks'

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ('method', 'path', 'params', 'headers', 'expected_status'),
    [
        ('GET', BOOKMARKS_URL_PATH, None, HEADER_WITH_TOKEN, HTTPStatus.OK),
        (
            'GET',
            BOOKMARKS_URL_PATH,
            {'page[size]': 60, 'page[number]': 1},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            BOOKMARKS_URL_PATH,
            {'page[size]': 0, 'page[number]': 1},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            BOOKMARKS_URL_PATH,
            {'page[size]': 20, 'page[number]': 0},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            BOOKMARKS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('GET', BOOKMARKS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_get_bookmarks(
    make_request, method, path, params, headers, expected_status
):
    response = await make_request(method, path, headers=headers, params=params)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'POST',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.CREATED,
        ),
        (
            'POST',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.CONFLICT,
        ),
        (
            'POST',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'POST',
            BOOKMARKS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'POST',
            BOOKMARKS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('POST', BOOKMARKS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_create_bookmark(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'DELETE',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NO_CONTENT,
        ),
        (
            'DELETE',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NOT_FOUND,
        ),
        (
            'DELETE',
            BOOKMARKS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            BOOKMARKS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            BOOKMARKS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('DELETE', BOOKMARKS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_delete_bookmark(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status
