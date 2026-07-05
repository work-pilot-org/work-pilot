import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.core.config import settings

ENV_PY_PATH = Path(__file__).resolve().parents[2] / "alembic" / "env.py"


def _install_fake_alembic(is_offline: bool):
    """
    Replace the top-level ``alembic`` package (and its ``context``
    submodule) in ``sys.modules`` with lightweight mocks so that
    ``alembic/env.py`` can be executed in isolation, without requiring a
    real database connection or a real Alembic runtime context.
    """
    fake_context = MagicMock(name="alembic.context")
    fake_context.is_offline_mode.return_value = is_offline

    fake_config = MagicMock(name="alembic.config.Config")
    fake_config.config_file_name = None
    fake_context.config = fake_config

    fake_alembic_pkg = types.ModuleType("alembic")
    fake_alembic_pkg.context = fake_context

    sys.modules["alembic"] = fake_alembic_pkg
    sys.modules["alembic.context"] = fake_context

    return fake_context, fake_config


def _load_env_module():
    spec = importlib.util.spec_from_file_location(
        "alembic_env_under_test", ENV_PY_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def _restore_alembic_modules():
    original_alembic = sys.modules.get("alembic")
    original_alembic_context = sys.modules.get("alembic.context")

    yield

    if original_alembic is not None:
        sys.modules["alembic"] = original_alembic
    else:
        sys.modules.pop("alembic", None)

    if original_alembic_context is not None:
        sys.modules["alembic.context"] = original_alembic_context
    else:
        sys.modules.pop("alembic.context", None)


class TestOfflineMigrations:
    def test_configures_sqlalchemy_url_from_settings(self):
        _fake_context, fake_config = _install_fake_alembic(is_offline=True)

        _load_env_module()

        fake_config.set_main_option.assert_any_call(
            "sqlalchemy.url", settings.DATABASE_URL
        )

    def test_runs_offline_migrations_with_literal_binds_and_schema_support(self):
        fake_context, _fake_config = _install_fake_alembic(is_offline=True)

        _load_env_module()

        fake_context.configure.assert_called_once()
        _, kwargs = fake_context.configure.call_args
        assert kwargs["literal_binds"] is True
        assert kwargs["include_schemas"] is True
        assert "connection" not in kwargs
        fake_context.begin_transaction.assert_called_once()
        fake_context.run_migrations.assert_called_once()


class TestOnlineMigrations:
    def test_runs_online_migrations_with_a_real_connection(self, monkeypatch):
        fake_context, _fake_config = _install_fake_alembic(is_offline=False)

        fake_connection = MagicMock(name="connection")
        fake_connectable = MagicMock(name="connectable")
        fake_connectable.connect.return_value.__enter__.return_value = (
            fake_connection
        )
        monkeypatch.setattr(
            "sqlalchemy.engine_from_config", lambda *a, **k: fake_connectable
        )

        _load_env_module()

        fake_context.configure.assert_called_once()
        _, kwargs = fake_context.configure.call_args
        assert kwargs["connection"] is fake_connection
        assert kwargs["include_schemas"] is True
        assert kwargs["compare_type"] is True
        fake_context.begin_transaction.assert_called_once()
        fake_context.run_migrations.assert_called_once()