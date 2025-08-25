from collections.abc import Callable
from typing import Any

from pydantic import AliasChoices, AmqpDsn, BaseModel, Field, ImportString, \
    PostgresDsn, RedisDsn, MongoDsn, field_validator


from typing import Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict, SettingsError


class GlobalSettings(BaseSettings):
    """
    Global application settings loaded from environment variables.
    """
    APP_NAME: str = Field(...,)
    SECRET_KEY: str = Field(...,)
    DEBUG: bool = Field(False,)
    BASE_URL: str = Field(...,)
    ENV_TYPE: str = Field(..., alias="ENV_TYPE")

    MONGO_URL: MongoDsn = Field(...,)
    MONGO_NAME: str = Field(...,)
    JWT_ALGORITHM: str = Field("HS256",)
    ALLOWED_HOSTS: Tuple[str, ...] | str = Field(("*",),)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8,)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 30 * 6,)

    LANGUAGE_CODE: str = Field("en-us",)
    TIME_ZONE: str = Field("UTC",)
    USE_I18N: bool = Field(True,)
    USE_TZ: bool = Field(True,)

    OTP_ATTEMPT_LIMIT: int = Field(5,)
    OTP_ATTEMPT_TIMEOUT: int = Field(10,)  # in minutes

    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8')

    @field_validator("ALLOWED_HOSTS", mode="before")
    def split_hosts(cls, value: Any) -> Tuple[str, ...]:
        if isinstance(value, str):
            result = tuple([item.strip() for item in value.split(",")])
            print(f"ALLOWED_HOSTS: {result}")
            return result
        return value
    
    # @classmethod
    # def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
    #     def parse_tuple(value: str):
    #         try:
    #             return tuple(item.strip() for item in value.split(","))
    #         except Exception:
    #             raise SettingsError("ALLOWED_HOSTS must be a comma-separated string")
    #     dotenv_settings["ALLOWED_HOSTS"] = parse_tuple(dotenv_settings.get("ALLOWED_HOSTS", "*"))
    #     return (init_settings, env_settings, dotenv_settings, file_secret_settings)


global_settings = GlobalSettings()
