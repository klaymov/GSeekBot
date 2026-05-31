import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import InlineQuery


class DebounceInlineMiddleware(BaseMiddleware):
    """
    Middleware that debounces inline queries.
    Waits `delay` seconds before passing the query to the handler.
    If a new query arrives from the same user within the delay,
    the previous one is cancelled.
    """
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.tasks: dict[int, asyncio.Task] = {}

    async def __call__(
        self,
        handler: Callable[[InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: InlineQuery,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        
        if user_id in self.tasks:
            self.tasks[user_id].cancel()
            
        async def delayed_handler():
            await asyncio.sleep(self.delay)
            return await handler(event, data)
            
        task = asyncio.create_task(delayed_handler())
        self.tasks[user_id] = task
        
        try:
            return await task
        except asyncio.CancelledError:
            return None
