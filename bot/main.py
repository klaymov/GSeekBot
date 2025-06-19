import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger

from .handlers import register_handlers
from .middlewares import register_middlewares
from core.config import Config
from core.logger import start_log
from database.connection import connect_to_mongo

        
async def startup(dispatcher: Dispatcher, bot: Bot, config: Config) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await start_log(bot)
    
    await connect_to_mongo(config)

    register_middlewares(dispatcher)
    dispatcher.include_router(register_handlers())
    
    logger.info("Bot started")


async def shutdown(dispatcher: Dispatcher) -> None:
    logger.info("Bot stopped")
    
    
async def main() -> None:
    config = Config()
    
    token = (
        config.prod_bot_token.get_secret_value() if not config.dev
        else config.dev_bot_token.get_secret_value()
    )

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(
        config=config,
        developer_ids=config.developer_ids,
    )

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
        
if __name__ == "__main__":
    asyncio.run(main())