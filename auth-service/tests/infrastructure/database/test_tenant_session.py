from unittest.mock import MagicMock

import pytest

from shared_infrastructure.database.tenant_session import (
    set_public_schema,
    set_tenant_schema,
)


class TestSetTenantSchema:
    @pytest.mark.parametrize(
        "schema_name",
        [
            "tenant_openai_india",
            "a",
            "tenant1",
            "tenant_123",
            "t",
        ],
    )
    def test_executes_set_search_path_for_valid_schema_names(self, schema_name):
        db = MagicMock()
        mock_connection = MagicMock()
        db.connection.return_value = mock_connection

        set_tenant_schema(db, schema_name)

        mock_connection.exec_driver_sql.assert_called_once_with(
            f'SET search_path TO "{schema_name}", public'
        )

    @pytest.mark.parametrize(
        "schema_name",
        [
            "tenant-name",
            "tenant name",
            "",
            'tenant"; DROP TABLE users; --',
            "tenant.public",
        ],
    )
    def test_raises_value_error_for_invalid_schema_names(self, schema_name):
        db = MagicMock()

        with pytest.raises(ValueError, match="Invalid schema name:"):
            set_tenant_schema(db, schema_name)


class TestSetPublicSchema:
    def test_executes_set_search_path_to_public(self):
        db = MagicMock()
        mock_connection = MagicMock()
        db.connection.return_value = mock_connection

        set_public_schema(db)

        mock_connection.exec_driver_sql.assert_called_once_with(
            'SET search_path TO "public"'
        )