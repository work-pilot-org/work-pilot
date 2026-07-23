from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="WorkPilot AI Service", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8004, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # AI Provider
    gemini_api_key: str = Field(alias="GEMINI_API_KEY")

    # Database
    database_url: str = Field(alias="DATABASE_URL")

    # Redis
    redis_url: str = Field(alias="REDIS_URL")

    # Microservices
    it_service_url: str = Field(alias="IT_SERVICE_URL")
    hr_service_url: str = Field(alias="HR_SERVICE_URL")
    workflow_service_url: str = Field(alias="WORKFLOW_SERVICE_URL")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()