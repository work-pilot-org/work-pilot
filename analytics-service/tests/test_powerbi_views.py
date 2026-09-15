import importlib.util
from pathlib import Path

import pytest
from shared_infrastructure.database.session import SessionLocal
from sqlalchemy import text

MIGRATION_PATH = Path(__file__).parent.parent / "alembic" / "versions" / "b6e8a719c2f1_add_power_bi_reporting_views.py"
spec = importlib.util.spec_from_file_location("migration_module", MIGRATION_PATH)
migration_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration_module)


EXPECTED_VIEWS = {
    "vw_attendance_reporting": [
        "date",
        "employee_id",
        "employee_name",
        "employment_type",
        "department",
        "designation",
        "branch",
        "check_in_time",
        "check_out_time",
        "attendance_status",
        "worked_minutes",
        "worked_hours",
        "late_minutes",
        "overtime_minutes",
    ],
    "vw_leave_reporting": [
        "date",
        "employee_id",
        "employee_name",
        "department",
        "leave_type",
        "leave_status",
        "leave_days_requested",
        "decision_time_minutes",
        "created_at",
    ],
    "vw_workforce_headcount_reporting": [
        "employee_id",
        "employee_name",
        "first_name",
        "last_name",
        "employment_type",
        "status",
        "department",
        "designation",
        "branch",
    ],
    "vw_it_tickets_reporting": [
        "date",
        "employee_id",
        "employee_name",
        "department",
        "priority",
        "status",
        "resolution_time_minutes",
        "first_response_minutes",
        "sla_breached",
        "created_at",
        "asset_name",
        "device_model",
        "software_title",
    ],
    "vw_asset_assignments_reporting": [
        "date",
        "asset_name",
        "asset_category",
        "asset_status",
        "employee_id",
        "employee_name",
        "assignment_id",
        "assigned_at",
        "returned_at",
        "assignment_duration_days",
        "assignment_status",
    ],
    "vw_workflow_performance_reporting": [
        "date",
        "workflow_name",
        "workflow_type",
        "execution_id",
        "initiator_employee_id",
        "initiator_employee_name",
        "execution_status",
        "total_completion_minutes",
        "step_count",
        "created_at",
        "last_event_occurred_at",
    ],
    "vw_workflow_bottlenecks_reporting": [
        "date",
        "workflow_name",
        "workflow_type",
        "execution_id",
        "workflow_step_id",
        "step_order",
        "entity_type",
        "approver_employee_id",
        "approver_employee_name",
        "status",
        "created_at",
        "decided_at",
        "decision_duration_seconds",
        "decision_duration_minutes",
        "decision_duration_hours",
    ],
}


def test_migration_metadata():
    """Verify revision and down_revision chain."""
    assert migration_module.revision == "b6e8a719c2f1"
    assert migration_module.down_revision == "4679833ff5a3"
    assert hasattr(migration_module, "upgrade")
    assert hasattr(migration_module, "downgrade")


def test_views_sql_definitions():
    """Verify all 7 views are defined in upgrade and dropped in downgrade."""
    import inspect
    upgrade_source = inspect.getsource(migration_module.upgrade)
    downgrade_source = inspect.getsource(migration_module.downgrade)

    for view_name in EXPECTED_VIEWS:
        assert f"CREATE OR REPLACE VIEW {view_name}" in upgrade_source
        assert f"DROP VIEW IF EXISTS {view_name}" in downgrade_source


def test_views_in_database():
    """
    Test creating views in a test database schema and verifying columns.
    If live database is not reachable, skip cleanly.
    """
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1;"))
    except Exception as exc:
        pytest.skip(f"Live database not reachable: {exc}")

    test_schema = "test_pbi_views_schema"
    try:
        # Create isolated temporary test schema
        session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {test_schema};"))
        session.execute(text(f'SET search_path TO "{test_schema}", public;'))

        # Create needed mock tables in test schema to validate view definitions
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_tenant (
                id BIGSERIAL PRIMARY KEY,
                tenant_id UUID NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_date (
                id INTEGER PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                day INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                quarter INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                is_weekend BOOLEAN NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_employee (
                id BIGSERIAL PRIMARY KEY,
                employee_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                first_name VARCHAR(150) NOT NULL,
                last_name VARCHAR(150) NOT NULL,
                employment_type VARCHAR(50),
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_department (
                id BIGSERIAL PRIMARY KEY,
                department_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                name VARCHAR(150) NOT NULL,
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_designation (
                id BIGSERIAL PRIMARY KEY,
                designation_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                name VARCHAR(150) NOT NULL,
                level INTEGER
            );
            CREATE TABLE IF NOT EXISTS dim_branch (
                id BIGSERIAL PRIMARY KEY,
                branch_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                name VARCHAR(150) NOT NULL,
                location VARCHAR(255)
            );
            CREATE TABLE IF NOT EXISTS dim_asset (
                id BIGSERIAL PRIMARY KEY,
                asset_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                name VARCHAR(150) NOT NULL DEFAULT 'Unknown',
                category VARCHAR(100) NOT NULL,
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_device (
                id BIGSERIAL PRIMARY KEY,
                device_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                device_type VARCHAR(100),
                os VARCHAR(100),
                model VARCHAR(150) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dim_software (
                id BIGSERIAL PRIMARY KEY,
                software_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                title VARCHAR(150) NOT NULL,
                publisher VARCHAR(150)
            );
            CREATE TABLE IF NOT EXISTS dim_workflow (
                id BIGSERIAL PRIMARY KEY,
                workflow_id UUID NOT NULL,
                tenant_id UUID NOT NULL,
                name VARCHAR(255) NOT NULL,
                workflow_type VARCHAR(100) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fact_attendance (
                id BIGSERIAL PRIMARY KEY,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                employee_key BIGINT NOT NULL,
                department_key BIGINT,
                designation_key BIGINT,
                branch_key BIGINT,
                source_event_id UUID NOT NULL,
                check_in_time TIMESTAMP,
                check_out_time TIMESTAMP,
                created_at TIMESTAMP NOT NULL,
                worked_minutes INTEGER,
                late_minutes INTEGER,
                overtime_minutes INTEGER,
                attendance_status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fact_leave (
                id BIGSERIAL PRIMARY KEY,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                employee_key BIGINT NOT NULL,
                department_key BIGINT,
                source_event_id UUID NOT NULL,
                created_at TIMESTAMP NOT NULL,
                leave_days_requested INTEGER NOT NULL,
                decision_time_minutes INTEGER,
                leave_status VARCHAR(50) NOT NULL,
                leave_type VARCHAR(100) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fact_it_ticket (
                id BIGSERIAL PRIMARY KEY,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                employee_key BIGINT NOT NULL,
                department_key BIGINT,
                asset_key BIGINT,
                device_key BIGINT,
                software_key BIGINT,
                source_event_id UUID NOT NULL,
                created_at TIMESTAMP NOT NULL,
                resolution_time_minutes INTEGER,
                first_response_minutes INTEGER,
                priority VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                sla_breached BOOLEAN NOT NULL DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS fact_workflow_execution (
                id BIGSERIAL PRIMARY KEY,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                employee_key BIGINT NOT NULL,
                workflow_key BIGINT NOT NULL,
                execution_id UUID NOT NULL,
                source_event_id UUID NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_event_occurred_at TIMESTAMP,
                total_completion_minutes INTEGER,
                step_count INTEGER,
                execution_status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fact_workflow_step (
                id BIGSERIAL PRIMARY KEY,
                execution_id UUID NOT NULL,
                workflow_step_id UUID NOT NULL,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                workflow_key BIGINT NOT NULL,
                approver_key BIGINT,
                source_event_id UUID NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                last_event_occurred_at TIMESTAMP,
                step_order INTEGER NOT NULL,
                entity_type VARCHAR(100) NOT NULL,
                created_at TIMESTAMP,
                decided_at TIMESTAMP,
                decision_duration_seconds INTEGER,
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fact_asset_assignment (
                id BIGSERIAL PRIMARY KEY,
                assignment_id UUID NOT NULL,
                tenant_key BIGINT NOT NULL,
                date_key INTEGER NOT NULL,
                asset_key BIGINT NOT NULL,
                employee_key BIGINT NOT NULL,
                source_event_id UUID NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                last_event_occurred_at TIMESTAMP NOT NULL,
                assigned_at TIMESTAMP NOT NULL,
                returned_at TIMESTAMP,
                assignment_duration_days INTEGER,
                assignment_status VARCHAR(50) NOT NULL
            );
        """))
        session.commit()

        # Run upgrade migration in this schema
        from unittest.mock import patch
        with patch.object(migration_module.op, "execute", side_effect=lambda sql: session.execute(text(sql))):
            migration_module.upgrade()
            session.commit()

        # Verify each view exists and columns match expected
        for view_name, expected_cols in EXPECTED_VIEWS.items():
            cols_res = session.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = '{test_schema}' AND table_name = '{view_name}';
            """)).fetchall()
            actual_cols = [r[0] for r in cols_res]
            for col in expected_cols:
                assert col in actual_cols, f"Column '{col}' missing from view '{view_name}'. Actual: {actual_cols}"

            # Verify query executes without error
            session.execute(text(f"SELECT * FROM {test_schema}.{view_name} LIMIT 1;"))

        # Test downgrade
        with patch.object(migration_module.op, "execute", side_effect=lambda sql: session.execute(text(sql))):
            migration_module.downgrade()
            session.commit()

        for view_name in EXPECTED_VIEWS:
            view_exists = session.execute(text(f"""
                SELECT table_name
                FROM information_schema.views
                WHERE table_schema = '{test_schema}' AND table_name = '{view_name}';
            """)).fetchall()
            assert len(view_exists) == 0, f"View '{view_name}' was not dropped by downgrade()"

    finally:
        session.execute(text(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE;"))
        session.commit()
        session.close()
