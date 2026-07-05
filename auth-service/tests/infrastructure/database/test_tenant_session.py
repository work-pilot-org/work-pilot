from unittest.mock import MagicMock

import pytest

from src.infrastructure.database.tenant_session import (
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

        set_tenant_schema(db, schema_name)

        db.execute.assert_called_once()
        executed_stmt = db.execute.call_args[0][0]
        assert str(executed_stmt) == f'SET search_path TO "{schema_name}"'

    @pytest.mark.parametrize(
        "schema_name",
        [
            "Tenant_Name",
            "1tenant",
            "tenant-name",
            "tenant name",
            "",
            'tenant"; DROP TABLE users; --',
            "tenant.public",
            "_tenant",
        ],
    )
    def test_raises_value_error_for_invalid_schema_names(self, schema_name):
        db = MagicMock()

        with pytest.raises(ValueError, match="Invalid schema name."):
            set_tenant_schema(db, schema_name)

        db.execute.assert_not_called()


class TestSetPublicSchema:
    def test_executes_set_search_path_to_public(self):
        db = MagicMock()

        set_public_schema(db)

        db.execute.assert_called_once()
        executed_stmt = db.execute.call_args[0][0]
        assert str(executed_stmt) == 'SET search_path TO "public"'