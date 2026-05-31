from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PSQL_", extra="ignore")

    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    bot_token: str
    openrouter_api_key: str
    rapidapi_key: str

    postgres: PostgresSettings = Field(default_factory=PostgresSettings)  # type: ignore

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()  # type: ignore
