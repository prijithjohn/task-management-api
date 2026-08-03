from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["development", "production", "testing"] = "development"
    database_url: str | None = None
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if self.environment == "production":
            return "postgresql+psycopg://postgres:postgres@localhost:5432/task_management"
        return "sqlite:///./task_management.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
