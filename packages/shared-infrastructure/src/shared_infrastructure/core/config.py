from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    FRONTEND_URL: str
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    RESET_TOKEN_EXPIRE_MINUTES: int
    
    SENDGRID_API_KEY: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()