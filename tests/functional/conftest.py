import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable

import aiohttp
import pytest_asyncio

from config import settings


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def make_request(
    session: aiohttp.ClientSession,
) -> Callable[..., Awaitable[aiohttp.ClientResponse]]:
    async def inner(
        method: str,
        suburl: str,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        body: dict | None = None,
    ) -> aiohttp.ClientResponse:
        url = f'{settings.ugc_url}{suburl}'
        return await session.request(
            method, url, params=params, headers=headers, json=body
        )

    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
def _prepare_test_env() -> None:
    from utils.depends import create_review

    asyncio.run(create_review())
