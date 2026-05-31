import asyncio
from typing import Any

from app.gseekbot.infrastructure.api.openrouter import OpenRouterClient
from app.gseekbot.infrastructure.api.rapidapi import RapidAPIClient


class SearchAggregatorService:
    def __init__(
        self, openrouter: OpenRouterClient, rapidapi: RapidAPIClient
    ) -> None:
        self.openrouter = openrouter
        self.rapidapi = rapidapi

    async def aggregate(self, query: str) -> dict[str, Any]:
        """
        Runs both AI and RapidAPI search concurrently.
        Returns a dict with 'ai' result and 'google' list of results.
        """
        ai_task = asyncio.create_task(self.openrouter.ask(query))
        google_task = asyncio.create_task(self.rapidapi.search(query))

        ai_res, google_res = await asyncio.gather(
            ai_task, google_task, return_exceptions=True
        )

        if isinstance(ai_res, Exception):
            ai_res = f"Помилка ШІ: {ai_res}"

        if isinstance(google_res, Exception):
            google_res = []

        return {
            "ai": ai_res,
            "google": google_res
        }
