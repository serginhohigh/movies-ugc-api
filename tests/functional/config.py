from pydantic import BaseSettings


class Settings(BaseSettings):
    ugc_host: str = 'test-ugc'
    ugc_port: int = 8000
    ugc_api_prefix: str = 'api/v1'
    ugc_url: str | None = None

    mongo_host: str = 'test-mongo'
    mongo_port: int = 27017
    mongo_database_uri: str | None = None

    jwt_secret_key: str
    jwt_algorithms: str

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self.ugc_url = f'http://{self.ugc_host}:{self.ugc_port}/{self.ugc_api_prefix}'
        self.mongo_database_uri = f'mongodb://{self.mongo_host}:{self.mongo_port}'


settings = Settings()
