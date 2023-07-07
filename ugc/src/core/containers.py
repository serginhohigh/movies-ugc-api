from dependency_injector import containers, providers

from db.mongo import MongoSearcher, init_mongo
from repositories.bookmarks import BookmarksRepository
from repositories.ratings import RatingsRepository
from repositories.reviews import ReviewsRepository
from services.bookmarks import BookmarksService
from services.ratings import RatingsService
from services.reviews import ReviewsService


class Container(containers.DeclarativeContainer):
    """Основной класс-контейнер для инициализации зависимостей."""

    config = providers.Configuration()

    mongo = providers.Resource(
        init_mongo,
        uri=config.mongo_database_uri,
    )

    bookmarks_repository = providers.Singleton(
        BookmarksRepository,
        mongo_client=mongo,
        database=config.mongo_db,
        collection=config.mongo_bookmarks_collection,
    )

    bookmarks_service = providers.Singleton(
        BookmarksService,
        bookmarks_repository=bookmarks_repository,
        searcher=MongoSearcher,
    )

    reviews_repository = providers.Singleton(
        ReviewsRepository,
        mongo_client=mongo,
        database=config.mongo_db,
        collection=config.mongo_reviews_collection,
    )

    reviews_service = providers.Singleton(
        ReviewsService,
        reviews_repository=reviews_repository,
        searcher=MongoSearcher,
    )

    ratings_repository = providers.Singleton(
        RatingsRepository,
        mongo_client=mongo,
        database=config.mongo_db,
        ratings_collection=config.mongo_ratings_collection,
        movies_collection=config.mongo_movies_collection,
    )

    ratings_service = providers.Singleton(
        RatingsService,
        ratings_repository=ratings_repository,
    )
