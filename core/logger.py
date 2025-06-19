import logging
from aiogram import Bot
from loguru import logger


def configure_logging() -> None:
    logger.add(
        "logs/bot_logs.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        rotation="5 MB",
        compression="zip",
    )
    
    logging.getLogger('aiogram').setLevel(logging.ERROR)
    logging.getLogger('asyncio').setLevel(logging.ERROR)


async def start_log(bot: Bot) -> None:
    try:
        configure_logging()
        bot_info = await bot.get_me()
        status_mapping = {
            True: "Enabled",
            False: "Disabled",
            None: "Unknown"
        }

        bot_attributes = {
            "Name": bot_info.full_name,
            "Username": f"@{bot_info.username}",
            "ID": bot_info.id,
            "Can Join Groups": status_mapping.get(bot_info.can_join_groups, 'N/A'),
            "Privacy Mode": status_mapping.get(not bot_info.can_read_all_group_messages, 'N/A'),
            "Inline Mode": status_mapping.get(bot_info.supports_inline_queries, 'N/A')
        }

        logger.info("Bot Information:")
        for attribute, value in bot_attributes.items():
            logger.info(f"{attribute}: {value}")
        
    except Exception as e:
        logger.exception(f"Failed to log bot info: {e}")