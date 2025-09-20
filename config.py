from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def varenv(varname):
    return Field(..., validation_alias=varname)


class EnvConf(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DeepSeek(EnvConf):
    ds_base_url: str = varenv("DEEPSEEK_BASE_URL")
    ds_api_key: str = varenv("DEEPSEEK_API_KEY")
    ds_model: str = varenv("DEEPSEEK_MODEL")


class Telegram(EnvConf):
    tg_bot_token: str = varenv("TG_BOT_TOKEN")



class EnvironmentSettings(BaseModel):
    deepseek: DeepSeek = Field(default_factory=DeepSeek)
    telegram: Telegram = Field(default_factory=Telegram)


config = EnvironmentSettings()
