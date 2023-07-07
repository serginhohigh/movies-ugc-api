import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import bookmarks, rating, reviews
from core.config import Settings, settings
from core.containers import Container
from core.logger import LOGGING


def create_app() -> FastAPI:
    """
    Функция для корректной инициализации приложения FastAPI.
    совместно с dependency_injector.
    """

    container = Container()
    container.config.from_pydantic(Settings())
    container.wire(packages=['api.v1'])

    app = FastAPI(
        title=settings.project_title,
        description=settings.project_description,
        version=settings.project_version,
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
        default_response_class=ORJSONResponse,
    )

    app.container = container  # type: ignore
    return app


if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
    )

app = create_app()

app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['Закладки'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['Рецензии'])
app.include_router(rating.router, prefix='/api/v1/rating', tags=['Рейтинг'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
