import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from config import settings


async def ping_server() -> None:
    client = AsyncIOMotorClient(settings.mongo_database_uri)

    while True:
        try:
            await client.admin.command('ping')
            break
        except (ConnectionFailure, ServerSelectionTimeoutError):
            time.sleep(2)
            continue


asyncio.run(ping_server())
