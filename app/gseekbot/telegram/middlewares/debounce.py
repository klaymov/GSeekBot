import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DebounceInlineMiddleware(BaseMiddleware):
    """
    Middleware that debounces inline queries.
    Waits `delay` seconds before passing the query to the handler.
    If a new query arrives from the same user within the delay,
    the previous one is cancelled.
    """

    def __init__(self, delay: float = 1.0) -> None:
        self.delay = delay
        self.tasks: dict[int, asyncio.Task] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = getattr(getattr(event, "from_user", None), "id", None)
        if not user_id:
            return await handler(event, data)

        if user_id in self.tasks:
            self.tasks[user_id].cancel()

        async def delayed_handler() -> Any:
            await asyncio.sleep(self.delay)
            return await handler(event, data)

        task = asyncio.create_task(delayed_handler())
        self.tasks[user_id] = task

        try:
            return await task
        except asyncio.CancelledError:
            return None
