from http import HTTPStatus

import pytest

from utils.depends import (
    HEADER_WITH_INDVALID_TOKEN,
    HEADER_WITH_TOKEN,
    MOVIE_UUID,
    MOVIE_UUID_INVALID,
    REVIEW_UUID,
)

REVIEWS_URL_PATH = '/reviews'

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'POST',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'text': 'ASDF'},
            HEADER_WITH_TOKEN,
            HTTPStatus.CREATED,
        ),
        (
            'POST',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'text': 'ASDF'},
            HEADER_WITH_TOKEN,
            HTTPStatus.CONFLICT,
        ),
        (
            'POST',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'POST',
            REVIEWS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'POST',
            REVIEWS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('POST', REVIEWS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_create_review(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'params', 'expected_status'),
    [
        (
            'GET',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HTTPStatus.OK,
        ),
        (
            'GET',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'page[size]': 60, 'page[number]': 1},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'page[size]': 0, 'page[number]': 1},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID, 'page[size]': 20, 'page[number]': 0},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'GET',
            REVIEWS_URL_PATH,
            None,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_get_rating(make_request, method, path, params, expected_status):
    response = await make_request(method, path, params=params)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'params', 'headers', 'expected_status'),
    [
        (
            'PATCH',
            REVIEWS_URL_PATH,
            {'review_id': REVIEW_UUID},
            {'action': 'add', 'type': 'like'},
            HEADER_WITH_TOKEN,
            HTTPStatus.NO_CONTENT,
        ),
        (
            'PATCH',
            REVIEWS_URL_PATH,
            {'review_id': REVIEW_UUID},
            {'action': 'add', 'type': 'like'},
            HEADER_WITH_TOKEN,
            HTTPStatus.CONFLICT,
        ),
        (
            'PATCH',
            REVIEWS_URL_PATH,
            {'review_id': REVIEW_UUID},
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'PATCH',
            REVIEWS_URL_PATH,
            None,
            {'action': 'add', 'type': 'like'},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'PATCH',
            REVIEWS_URL_PATH,
            None,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('PATCH', REVIEWS_URL_PATH, None, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_rate_review(
    make_request, method, path, body, params, headers, expected_status
):
    response = await make_request(
        method, path, headers=headers, body=body, params=params
    )
    assert response.status == expected_status


@pytest.mark.parametrize(
    ('method', 'path', 'body', 'headers', 'expected_status'),
    [
        (
            'DELETE',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NO_CONTENT,
        ),
        (
            'DELETE',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID},
            HEADER_WITH_TOKEN,
            HTTPStatus.NOT_FOUND,
        ),
        (
            'DELETE',
            REVIEWS_URL_PATH,
            {'movie_id': MOVIE_UUID_INVALID},
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            REVIEWS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            'DELETE',
            REVIEWS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.UNAUTHORIZED,
        ),
        ('DELETE', REVIEWS_URL_PATH, None, None, HTTPStatus.FORBIDDEN),
    ],
)
async def test_delete_review(
    make_request, method, path, body, headers, expected_status
):
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status
