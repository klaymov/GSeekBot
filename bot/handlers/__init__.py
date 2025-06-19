from aiogram import Router
from loguru import logger

from . import (
    inline,
    message,
)

def register_handlers():
    router = Router()
    router.include_routers(
        inline.router,
        message.router,
    )
    
    logger.success("Handlers registered")
    return router