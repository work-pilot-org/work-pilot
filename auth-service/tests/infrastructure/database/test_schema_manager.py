from unittest.mock import MagicMock

from shared_infrastructure.database.base import TenantBase
from src.infrastructure.database.schema_manager import SchemaManager


class TestCreateSchema:
    def test_executes_create_schema_statement_with_the_given_schema_name(self):
        db = MagicMock()
        mock_connection = MagicMock()
        db.connection.return_value = mock_connection

        SchemaManager.create_schema(db, "tenant_openai_india")

        mock_connection.exec_driver_sql.assert_called_once_with(
            'CREATE SCHEMA "tenant_openai_india"'
        )

    def test_wraps_schema_name_in_double_quotes(self):
        db = MagicMock()
        mock_connection = MagicMock()
        db.connection.return_value = mock_connection

        SchemaManager.create_schema(db, "my_schema")

        mock_connection.exec_driver_sql.assert_called_once_with(
            'CREATE SCHEMA "my_schema"'
        )

    def test_uses_the_provided_session_to_execute(self):
        db = MagicMock()
        mock_connection = MagicMock()
        db.connection.return_value = mock_connection

        SchemaManager.create_schema(db, "another_schema")

        db.connection.assert_called_once()


class TestCreateTenantTables:
    def test_obtains_a_connection_from_the_session(self):
        db = MagicMock()
        fake_connection = MagicMock()
        db.connection.return_value = fake_connection

        SchemaManager.create_tenant_tables(db, "tenant_test")

        db.connection.assert_called_once_with()

    def test_creates_all_tenant_base_tables_bound_to_the_connection(
        self, monkeypatch
    ):
        db = MagicMock()
        fake_connection = MagicMock()
        db.connection.return_value = fake_connection

        mock_create_all = MagicMock()
        monkeypatch.setattr(TenantBase.metadata, "create_all", mock_create_all)

        SchemaManager.create_tenant_tables(db, "tenant_test")

        mock_create_all.assert_called_once_with(bind=fake_connection)
