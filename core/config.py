from typing import List
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )
    dev: bool = Field(False, env="DEV")
    developer_ids: List[int] = Field(..., env="DEVELOPER_IDS", env_delimiter=",")

    dev_bot_token: SecretStr = Field(..., env="DEV_BOT_TOKEN")
    prod_bot_token: SecretStr = Field(..., env="PROD_BOT_TOKEN")

    db_url: str = Field(..., env="DB_URL")
    db_name: str = Field(..., env="DB_NAME")

config = Config()