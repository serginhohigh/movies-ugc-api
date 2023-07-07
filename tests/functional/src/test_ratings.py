from http import HTTPStatus

import pytest

from utils.depends import (
    HEADER_WITH_INDVALID_TOKEN,
    HEADER_WITH_TOKEN,
    MOVIE_UUID,
    MOVIE_UUID_INVALID,
)

RATINGS_URL_PATH = '/rating'

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'PUT',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'rating': 5},
            HEADER_WITH_TOKEN,
            HTTPStatus.CREATED,
        ),
        (
            'PUT',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'rating': 5},
            HEADER_WITH_TOKEN,
            HTTPStatus.CONFLICT,
        ),
        (
            'PUT',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'PUT',
            RATINGS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'PUT',
            RATINGS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('PUT', RATINGS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_create_rating(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'params', 'expected_status'),
    [
        (
            'GET',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HTTPStatus.OK,
        ),
        (
            'GET',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            RATINGS_URL_PATH,
            None,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_get_rating(make_request, method, path, params, expected_status):
    response = await make_request(method, path, params=params)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'DELETE',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NO_CONTENT,
        ),
        (
            'DELETE',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NOT_FOUND,
        ),
        (
            'DELETE',
            RATINGS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            RATINGS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            RATINGS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('DELETE', RATINGS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_delete_rating(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status
