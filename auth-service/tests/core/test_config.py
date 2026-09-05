import pytest
from pydantic import ValidationError

from shared_infrastructure.core.config import Settings


REQUIRED_ENV = {
    "APP_NAME": "Auth Service",
    "DEBUG": "True",
    "DATABASE_URL": "postgresql+psycopg://user:pass@localhost:5432/db",
    "SECRET_KEY": "super-secret-key",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "REFRESH_TOKEN_EXPIRE_DAYS": "7",
}


def _set_env(monkeypatch, overrides=None, remove=None):
    env = {**REQUIRED_ENV, **(overrides or {})}
    for key in remove or []:
        env.pop(key, None)
    for key, value in env.items():
        monkeypatch.setenv(key, value)


class TestSettingsLoadsFromEnvironment:
    def test_loads_all_fields_from_env_vars(self, monkeypatch):
        _set_env(monkeypatch)

        settings = Settings(_env_file=None)

        assert settings.APP_NAME == "Auth Service"
        assert settings.DEBUG is True
        assert settings.DATABASE_URL == REQUIRED_ENV["DATABASE_URL"]
        assert settings.SECRET_KEY == "super-secret-key"
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7

    def test_access_token_expire_minutes_is_coerced_to_int(self, monkeypatch):
        _set_env(monkeypatch, overrides={"ACCESS_TOKEN_EXPIRE_MINUTES": "45"})

        settings = Settings(_env_file=None)

        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 45
        assert isinstance(settings.ACCESS_TOKEN_EXPIRE_MINUTES, int)

    def test_refresh_token_expire_days_is_coerced_to_int(self, monkeypatch):
        _set_env(monkeypatch, overrides={"REFRESH_TOKEN_EXPIRE_DAYS": "14"})

        settings = Settings(_env_file=None)

        assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 14
        assert isinstance(settings.REFRESH_TOKEN_EXPIRE_DAYS, int)

    def test_extra_env_vars_are_ignored(self, monkeypatch):
        _set_env(monkeypatch, overrides={"SOME_UNRELATED_VAR": "value"})

        settings = Settings(_env_file=None)

        assert not hasattr(settings, "SOME_UNRELATED_VAR")


class TestSettingsValidation:
    def test_missing_refresh_token_expire_days_fallback(
        self, monkeypatch
    ):
        _set_env(monkeypatch, remove=["REFRESH_TOKEN_EXPIRE_DAYS"])
        settings = Settings(_env_file=None)
        assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7

    def test_invalid_refresh_token_expire_days_raises_validation_error(
        self, monkeypatch
    ):
        _set_env(monkeypatch, overrides={"REFRESH_TOKEN_EXPIRE_DAYS": "not-a-number"})

        with pytest.raises(ValidationError):
            Settings(_env_file=None)

    def test_missing_secret_key_fallback(self, monkeypatch):
        _set_env(monkeypatch, remove=["SECRET_KEY"])
        settings = Settings(_env_file=None)
        assert isinstance(settings.SECRET_KEY, str)

    def test_invalid_debug_value_raises_validation_error(self, monkeypatch):
        _set_env(monkeypatch, overrides={"DEBUG": "not-a-bool"})

        with pytest.raises(ValidationError):
            Settings(_env_file=None)
