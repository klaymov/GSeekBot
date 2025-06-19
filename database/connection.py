from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from loguru import logger

from core.config import Config
from .models import user


async def connect_to_mongo(config: Config) -> None:
    db_name = config.db_name if not config.dev else f"{config.db_name}_dev"
    client = AsyncIOMotorClient(config.db_url)
    await init_beanie(
        database=client[db_name],
        document_models=[
            user.UserModel
        ]
    )
    
    logger.success("Connected to MongoDB")