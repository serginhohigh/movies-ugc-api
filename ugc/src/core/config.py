from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_title: str = 'PROJECT_TITLE'
    project_description: str = 'PROJECT_DESCRIPTION'
    project_version: str = 'PROJECT_VERSION'
    docs_url: str = '/api/v1/swagger'
    openapi_url: str = '/api/v1/openapi.json'

    mongo_host: str
    mongo_port: str
    mongo_db: str
    mongo_user: str
    mongo_password: str
    mongo_bookmarks_collection: str
    mongo_reviews_collection: str
    mongo_ratings_collection: str
    mongo_movies_collection: str

    mongo_database_uri: str | None = None

    jwt_secret_key: str
    jwt_algorithms: str

    sentry_dsn: str | None = None

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)

        self.mongo_database_uri = (
            f'mongodb://{self.mongo_user}:{self.mongo_password}'
            f'@{self.mongo_host}:{self.mongo_port}/{self.mongo_db}'
        )


def get_settings() -> Settings:
    return Settings()


settings = Settings()
