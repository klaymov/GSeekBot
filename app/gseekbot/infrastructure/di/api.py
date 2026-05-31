from typing import AsyncIterable

import aiohttp
from dishka import Provider, Scope, provide

from app.gseekbot.config import Settings
from app.gseekbot.infrastructure.api.openrouter import OpenRouterClient
from app.gseekbot.infrastructure.api.rapidapi import RapidAPIClient


class ApiProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_client_session(self) -> AsyncIterable[aiohttp.ClientSession]:
        async with aiohttp.ClientSession() as session:
            yield session

    @provide
    def get_openrouter_client(
        self, session: aiohttp.ClientSession, settings: Settings
    ) -> OpenRouterClient:
        return OpenRouterClient(api_key=settings.openrouter_api_key, session=session)

    @provide
    def get_rapidapi_client(
        self, session: aiohttp.ClientSession, settings: Settings
    ) -> RapidAPIClient:
        return RapidAPIClient(api_key=settings.rapidapi_key, session=session)
