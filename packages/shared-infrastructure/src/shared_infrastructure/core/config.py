from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "WorkPilot"
    APP_VERSION: str = "1.0.0"
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

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LLM_PROVIDER: str = "gemini"
    LOG_LEVEL: str = "INFO"

    # Service URLs
    IT_SERVICE_URL: str | None = None
    HR_SERVICE_URL: str | None = None
    WORKFLOW_SERVICE_URL: str | None = None
    NOTIFICATION_SERVICE_URL: str | None = None
    AI_SERVICE_URL: str | None = None
    AUTH_SERVICE_URL: str | None = None

    @property
    def app_name(self) -> str:
        return self.APP_NAME

    @property
    def app_version(self) -> str:
        return self.APP_VERSION

    @property
    def debug(self) -> bool:
        return self.DEBUG

    @property
    def database_url(self) -> str | None:
        return self.DATABASE_URL

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def algorithm(self) -> str:
        return self.ALGORITHM

    @property
    def access_token_expire_minutes(self) -> int:
        return self.ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def refresh_token_expire_days(self) -> int:
        return self.REFRESH_TOKEN_EXPIRE_DAYS

    @property
    def frontend_url(self) -> str:
        return self.FRONTEND_URL

    @property
    def password_reset_expire_minutes(self) -> int:
        return self.PASSWORD_RESET_EXPIRE_MINUTES

    @property
    def reset_token_expire_minutes(self) -> int | None:
        return self.RESET_TOKEN_EXPIRE_MINUTES

    @property
    def sendgrid_api_key(self) -> str | None:
        return self.SENDGRID_API_KEY

    @property
    def email_from(self) -> str | None:
        return self.EMAIL_FROM

    @property
    def email_from_name(self) -> str | None:
        return self.EMAIL_FROM_NAME

    @property
    def gemini_api_key(self) -> str | None:
        return self.GEMINI_API_KEY

    @property
    def gemini_model(self) -> str:
        return self.GEMINI_MODEL

    @property
    def llm_provider(self) -> str:
        return self.LLM_PROVIDER

    @property
    def log_level(self) -> str:
        return self.LOG_LEVEL

    @property
    def it_service_url(self) -> str | None:
        return self.IT_SERVICE_URL

    @property
    def hr_service_url(self) -> str | None:
        return self.HR_SERVICE_URL

    @property
    def workflow_service_url(self) -> str | None:
        return self.WORKFLOW_SERVICE_URL

    @property
    def notification_service_url(self) -> str | None:
        return self.NOTIFICATION_SERVICE_URL

    @property
    def ai_service_url(self) -> str | None:
        return self.AI_SERVICE_URL

    @property
    def auth_service_url(self) -> str | None:
        return self.AUTH_SERVICE_URL


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
