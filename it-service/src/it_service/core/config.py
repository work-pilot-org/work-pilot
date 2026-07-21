from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    app_name: str = Field(default="WorkPilot IT Service", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8001, alias="API_PORT")

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    database_url: str = Field(alias="DATABASE_URL")

    # ------------------------------------------------------------------
    # External Services
    # ------------------------------------------------------------------
    auth_service_url: str = Field(alias="AUTH_SERVICE_URL")
    notification_service_url: str = Field(alias="NOTIFICATION_SERVICE_URL")

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def DATABASE_URL(self) -> str:
        return self.database_url

    @property
    def DEBUG(self) -> bool:
        return self.environment == "development"



@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The configuration is loaded only once during the application's lifetime.
    """
    return Settings()


settings = get_settings()