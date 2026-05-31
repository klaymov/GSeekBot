from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.gseekbot.infrastructure.db.models.user import UserModel, utc_now

if TYPE_CHECKING:
    from aiogram_i18n import I18nContext
    from dishka import AsyncContainer


def resolve_locale(language_code: str | None) -> str:
    """
    Checks if there is a locale directory for the given language_code.
    If yes, returns the language_code. Otherwise returns 'en'.
    """
    if not language_code:
        return "en"

    locales_dir = Path("app/gseekbot/locales")
    code = language_code.split("-")[0]

    if (locales_dir / code).is_dir():
        return code
    return "en"


class UserMiddleware(BaseMiddleware):
    """
    Middleware that ensures the user exists in the database.
    Updates last_active, is_premium, locale, and pm_active.
    Passes user_model to the handler data.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        is_pm = False
        chat = data.get("event_chat")
        if chat and chat.type == "private":
            is_pm = True

        locale = resolve_locale(user.language_code)

        container: AsyncContainer = data["dishka_container"]
        session: AsyncSession = await container.get(AsyncSession)

        db_user = await session.get(UserModel, user.id)
        if db_user:
            db_user.username = user.username
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.is_premium = user.is_premium or False
            db_user.last_active = utc_now()
            if is_pm:
                db_user.pm_active = True
            db_user.locale = locale
        else:
            db_user = UserModel(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_premium=user.is_premium or False,
                locale=locale,
                pm_active=is_pm,
            )
            session.add(db_user)

        await session.commit()

        # Inject into data for handlers
        data["user_model"] = db_user

        # Synchronize aiogram_i18n locale
        i18n: I18nContext | None = data.get("i18n")
        if i18n:
            i18n.locale = db_user.locale

        return await handler(event, data)
