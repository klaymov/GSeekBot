from __future__ import annotations

from aiogram import Router
from aiogram.types import (
    Message,
)
from translate import Translator
from loguru import logger

router = Router()


async def translate_text(text: str, language_code: str) -> str:
    if language_code != 'en':
        try:
            translator = Translator(to_lang=language_code)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            logger.exception(e)
            return text
    return text


@router.message()
async def message_handler(
    message: Message,
):
    if message.via_bot:
        return
    
    blog = '<a href="https://t.me/qublog">Blog</a>'
    github = '<a href="https://github.com/klaymov/GSeekBot">GitHub</a>'
    
    message_text = "Use @GSeekBot in any chat to search for information on Internet."
    message_text += "\n\nFor example: <code>@GSeekBot What is a metaphor?</code>"
    message_text += f"\n\n{blog}, {github}"
    
    await message.answer(
        text=await translate_text(message_text, message.from_user.language_code),
        disable_web_page_preview=True
    )

