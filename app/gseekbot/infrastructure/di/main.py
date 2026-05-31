from dishka import make_async_container, Provider, Scope, provide

from app.gseekbot.config import get_settings, Settings
from app.gseekbot.infrastructure.di.api import ApiProvider
from app.gseekbot.infrastructure.di.database import DatabaseProvider
from app.gseekbot.infrastructure.di.services import ServiceProvider


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> Settings:
        return get_settings()


def setup_container():
    return make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        ApiProvider(),
        ServiceProvider(),
    )
