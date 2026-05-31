from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from app.gseekbot.config import Settings, get_settings
from app.gseekbot.infrastructure.di.api import ApiProvider
from app.gseekbot.infrastructure.di.database import DatabaseProvider
from app.gseekbot.infrastructure.di.services import ServiceProvider


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> Settings:
        return get_settings()


def setup_container() -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        ApiProvider(),
        ServiceProvider(),
    )
