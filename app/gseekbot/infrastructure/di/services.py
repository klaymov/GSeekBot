from dishka import Provider, Scope, provide

from app.gseekbot.core.services.search_aggregator import SearchAggregatorService
from app.gseekbot.infrastructure.api.openrouter import OpenRouterClient
from app.gseekbot.infrastructure.api.rapidapi import RapidAPIClient


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def get_search_aggregator(
        self, openrouter: OpenRouterClient, rapidapi: RapidAPIClient
    ) -> SearchAggregatorService:
        return SearchAggregatorService(openrouter=openrouter, rapidapi=rapidapi)
