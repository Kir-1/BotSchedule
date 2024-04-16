from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent

    BOT_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/env/bot_schedule_example.env"
    )


settings = Settings()
