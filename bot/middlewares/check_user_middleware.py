from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final
from datetime import datetime, timezone

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject, Update, User, Chat

from database.models.user import UserModel

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


# 777000 is Telegram's user id of service messages
TG_SERVICE_USER_ID: Final[int] = 777000


async def _get_or_create_user(user: User, chat: Chat) -> UserModel:
    user_model: UserModel | None = await UserModel.get(user.id)
    if user_model:
        user_model = await _update_user(user_model, user)
        return user_model

    user_model = UserModel(
        id=user.id,
        
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        is_premium=user.is_premium,
        
        pm_active=getattr(chat, "type", None) == ChatType.PRIVATE if chat else False,
    )
    await user_model.insert()
    return user_model


async def _update_user(user_model: UserModel, user: User) -> None:
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.language_code = user.language_code
    user_model.is_premium = user.is_premium
    
    user_model.last_seen = datetime.now(timezone.utc)

    await user_model.save()
    return user_model


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        data["user_model"] = None
        user: User = data.get("event_from_user")
        chat: Chat = data.get("event_chat")

        match event.event_type:
            case "message" | "inline_query":
                if user.is_bot is False and user.id != TG_SERVICE_USER_ID:
                    data["user_model"] = await _get_or_create_user(
                        user,
                        chat,
                    )

            case _:
                pass

        return await handler(event, data)
