from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject, Update

ALLOWED_CHAT_TYPES: frozenset[ChatType] = frozenset((ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP))


class CheckChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        chat = data.get("event_chat")
        if chat and chat.type in ALLOWED_CHAT_TYPES:
            return

        return await handler(event, data)