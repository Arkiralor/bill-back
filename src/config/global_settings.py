from collections.abc import Callable
from typing import Any

from pydantic import AliasChoices, AmqpDsn, BaseModel, Field, ImportString, \
    PostgresDsn, RedisDsn, MongoDsn, field_validator, field_serializer

from os import path
from pathlib import Path
from typing import Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict, SettingsError


class GlobalSettings(BaseSettings):
    """
    Global application settings loaded from environment variables.
    """
    APP_NAME: str = Field(...,)
    SECRET_KEY: str = Field(...,)
    BASE_DIR: str = str(Path(path.dirname(path.abspath(__file__))).parent.parent)
    DEBUG: bool = Field(False,)
    BASE_URL: str = Field(...,)
    BASE_PORT: int = Field(8000,)
    ENV_TYPE: str = Field(..., alias="ENV_TYPE")

    MONGO_URL: MongoDsn = Field(...,)
    MONGO_NAME: str = Field(...,)
    JWT_ALGORITHM: str = Field("HS256",)
    ALLOWED_HOSTS: Tuple[str, ...] | str = Field(("*",),)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(5,)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 30 * 6,)

    LANGUAGE_CODE: str = Field("en-us",)
    TIME_ZONE: str = Field("UTC",)
    USE_I18N: bool = Field(True,)
    USE_TZ: bool = Field(True,)

    OTP_ATTEMPT_LIMIT: int = Field(5,)
    OTP_ATTEMPT_TIMEOUT: int = Field(10,)  # in minutes

    model_config = SettingsConfigDict(
        env_file='src/.env', env_file_encoding='utf-8')

    @field_validator("ALLOWED_HOSTS", mode="before")
    def split_hosts(cls, value: Any) -> Tuple[str, ...]:
        if isinstance(value, str):
            result = tuple([item.strip() for item in value.split(",")])
            return result
        return value
    
class ShowSettingsSchema(BaseModel):
    APP_NAME: str
    SECRET_KEY: str
    DEBUG: bool
    BASE_URL: str
    BASE_PORT: int
    ENV_TYPE: str
    MONGO_URL: str
    MONGO_NAME: str
    JWT_ALGORITHM: str
    ALLOWED_HOSTS: Tuple[str, ...] | str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    LANGUAGE_CODE: str
    TIME_ZONE: str
    USE_I18N: bool
    USE_TZ: bool
    OTP_ATTEMPT_LIMIT: int
    OTP_ATTEMPT_TIMEOUT: int

    @field_serializer("MONGO_URL", when_used="json")
    def serialize_mongo_url(self, value: Any) -> str:
        return f"{value}"


global_settings = GlobalSettings()
