from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "WorkPilot"
    DEBUG: bool = False
    
    DATABASE_URL: str | None = None
    
    SECRET_KEY: str = "default_secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    FRONTEND_URL: str = "http://localhost:3000"
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    RESET_TOKEN_EXPIRE_MINUTES: int | None = None
    
    SENDGRID_API_KEY: str | None = None
    EMAIL_FROM: str | None = None
    EMAIL_FROM_NAME: str | None = None
    
    # Service URLs
    IT_SERVICE_URL: str | None = None
    HR_SERVICE_URL: str | None = None
    WORKFLOW_SERVICE_URL: str | None = None
    NOTIFICATION_SERVICE_URL: str | None = None
    AI_SERVICE_URL: str | None = None
    AUTH_SERVICE_URL: str | None = None


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()