from aiogram import Dispatcher
from loguru import logger

from . import (
    logging_middleware,
    throttling_middleware,
    check_user_middleware,
    check_chat_middleware,
)


def register_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(logging_middleware.loggerMiddleware())
    
    dispatcher.message.middleware(throttling_middleware.ThrottlingMiddleware())
    
    dispatcher.update.outer_middleware(check_user_middleware.CheckUserMiddleware())
    dispatcher.update.outer_middleware(check_chat_middleware.CheckChatMiddleware())
    
    logger.success("Middlewares registered")