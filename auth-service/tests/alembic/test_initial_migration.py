import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import sqlalchemy as sa

MIGRATION_PATH = (
    Path(__file__).resolve().parents[2]
    / "alembic"
    / "versions"
    / "7b9352dd17b6_initial_migration.py"
)


def _load_migration_module():
    spec = importlib.util.spec_from_file_location(
        "initial_migration_under_test", MIGRATION_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def migration_module():
    return _load_migration_module()


class TestRevisionIdentifiers:
    def test_revision_id(self, migration_module):
        assert migration_module.revision == "7b9352dd17b6"

    def test_has_no_down_revision(self, migration_module):
        assert migration_module.down_revision is None

    def test_has_no_branch_labels(self, migration_module):
        assert migration_module.branch_labels is None

    def test_has_no_dependencies(self, migration_module):
        assert migration_module.depends_on is None


class TestUpgrade:
    def test_creates_tables_in_dependency_order(self, migration_module, monkeypatch):
        mock_op = MagicMock()
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.upgrade()

        created_tables = [
            call.args[0] for call in mock_op.create_table.call_args_list
        ]
        assert created_tables == ["tenants", "users", "domains", "user_profiles"]

    def test_creates_expected_indexes_with_correct_uniqueness(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        mock_op.f.side_effect = lambda name: name
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.upgrade()

        index_specs = {
            call.args[0]: {
                "table": call.args[1],
                "columns": call.args[2],
                "unique": call.kwargs.get("unique"),
            }
            for call in mock_op.create_index.call_args_list
        }

        assert index_specs["ix_tenants_id"] == {
            "table": "tenants",
            "columns": ["id"],
            "unique": False,
        }
        assert index_specs["ix_tenants_schema_name"] == {
            "table": "tenants",
            "columns": ["schema_name"],
            "unique": True,
        }
        assert index_specs["ix_users_email"] == {
            "table": "users",
            "columns": ["email"],
            "unique": True,
        }
        assert index_specs["ix_domains_domain"] == {
            "table": "domains",
            "columns": ["domain"],
            "unique": True,
        }
        assert index_specs["ix_domains_id"] == {
            "table": "domains",
            "columns": ["id"],
            "unique": False,
        }

    def test_domains_table_has_a_cascading_foreign_key_to_tenants(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.upgrade()

        domains_call = next(
            call
            for call in mock_op.create_table.call_args_list
            if call.args[0] == "domains"
        )
        fk_constraints = [
            arg
            for arg in domains_call.args[1:]
            if isinstance(arg, sa.ForeignKeyConstraint)
        ]

        assert len(fk_constraints) == 1
        assert fk_constraints[0].ondelete == "CASCADE"

    def test_user_profiles_table_has_cascading_foreign_keys(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.upgrade()

        user_profiles_call = next(
            call
            for call in mock_op.create_table.call_args_list
            if call.args[0] == "user_profiles"
        )
        fk_constraints = [
            arg
            for arg in user_profiles_call.args[1:]
            if isinstance(arg, sa.ForeignKeyConstraint)
        ]

        assert len(fk_constraints) == 2
        assert all(fk.ondelete == "CASCADE" for fk in fk_constraints)

    def test_user_profiles_has_a_unique_constraint(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.upgrade()

        user_profiles_call = next(
            call
            for call in mock_op.create_table.call_args_list
            if call.args[0] == "user_profiles"
        )
        unique_constraints = [
            arg
            for arg in user_profiles_call.args[1:]
            if isinstance(arg, sa.UniqueConstraint)
        ]

        assert len(unique_constraints) == 1


class TestDowngrade:
    def test_drops_tables_in_reverse_dependency_order(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.downgrade()

        dropped_tables = [call.args[0] for call in mock_op.drop_table.call_args_list]
        assert dropped_tables == ["user_profiles", "domains", "users", "tenants"]

    def test_drops_dependent_indexes_before_dropping_the_domains_table(
        self, migration_module, monkeypatch
    ):
        mock_op = MagicMock()
        mock_op.f.side_effect = lambda name: name
        monkeypatch.setattr(migration_module, "op", mock_op)

        migration_module.downgrade()

        call_sequence = []
        for method_call in mock_op.method_calls:
            name = method_call[0]
            if name == "drop_index":
                call_sequence.append(("drop_index", method_call.kwargs.get("table_name")))
            elif name == "drop_table":
                call_sequence.append(("drop_table", method_call.args[0]))

        domains_index_positions = [
            i
            for i, (op_name, target) in enumerate(call_sequence)
            if op_name == "drop_index" and target == "domains"
        ]
        domains_table_position = next(
            i
            for i, (op_name, target) in enumerate(call_sequence)
            if op_name == "drop_table" and target == "domains"
        )

        assert domains_index_positions
        assert all(pos < domains_table_position for pos in domains_index_positions)