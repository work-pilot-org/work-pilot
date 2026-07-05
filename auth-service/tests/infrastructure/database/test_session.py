from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.infrastructure.database import session as session_module


class TestEngineConfiguration:
    def test_engine_is_bound_to_the_configured_database_url(self):
        assert (
            session_module.engine.url.render_as_string(hide_password=False)
            == settings.DATABASE_URL
        )

    def test_session_local_is_a_sessionmaker_bound_to_the_engine(self):
        assert isinstance(session_module.SessionLocal, sessionmaker)
        assert session_module.SessionLocal.kw["bind"] is session_module.engine


class TestGetDb:
    def test_yields_a_session_instance(self, monkeypatch):
        fake_session = MagicMock()
        monkeypatch.setattr(session_module, "SessionLocal", lambda: fake_session)

        generator = session_module.get_db()
        db = next(generator)

        assert db is fake_session

    def test_closes_the_session_once_the_generator_is_exhausted(self, monkeypatch):
        fake_session = MagicMock()
        monkeypatch.setattr(session_module, "SessionLocal", lambda: fake_session)

        generator = session_module.get_db()
        next(generator)

        with pytest.raises(StopIteration):
            next(generator)

        fake_session.close.assert_called_once()

    def test_closes_the_session_even_if_an_exception_is_raised_during_use(
        self, monkeypatch
    ):
        fake_session = MagicMock()
        monkeypatch.setattr(session_module, "SessionLocal", lambda: fake_session)

        generator = session_module.get_db()
        next(generator)

        with pytest.raises(RuntimeError):
            generator.throw(RuntimeError("boom"))

        fake_session.close.assert_called_once()

    def test_creates_a_new_session_for_each_call(self, monkeypatch):
        created_sessions = [MagicMock(), MagicMock()]
        monkeypatch.setattr(
            session_module, "SessionLocal", MagicMock(side_effect=created_sessions)
        )

        first_db = next(session_module.get_db())
        second_db = next(session_module.get_db())

        assert first_db is created_sessions[0]
        assert second_db is created_sessions[1]
        assert first_db is not second_db