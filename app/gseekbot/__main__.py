import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dishka.integrations.aiogram import setup_dishka

from app.gseekbot.config import get_settings
from app.gseekbot.infrastructure.di.main import setup_container
from app.gseekbot.telegram.handlers.inline import router as inline_router
from app.gseekbot.telegram.middlewares.debounce import DebounceInlineMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    container = setup_container()
    settings = get_settings()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="app/gseekbot/locales/{locale}"),
        default_locale="uk",
    )
    i18n_middleware.setup(dp)

    dp.inline_query.middleware(DebounceInlineMiddleware(delay=1.0))
    dp.include_router(inline_router)

    setup_dishka(container=container, router=dp)

    try:
        await dp.start_polling(bot)
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
