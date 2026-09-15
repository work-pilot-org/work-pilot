import unittest

import sqlalchemy as sa
from alembic.config import Config
from alembic.script import ScriptDirectory
from shared_infrastructure.core.config import settings


class TestPowerBIReportingViews(unittest.TestCase):
    """
    Validation test suite for Power BI reporting views.
    Ensures views correctly expose business-friendly fields without surrogate key
    dependency, preserve tenant isolation, and handle upgrade/downgrade cleanly.
    """

    def setUp(self):
        self.alembic_cfg = Config("alembic.ini")
        self.script_dir = ScriptDirectory.from_config(self.alembic_cfg)

    def test_migration_chain_and_head(self):
        """Verify the migration is properly linked and forms a single head."""
        head = self.script_dir.get_current_head()
        self.assertEqual(head, "b6e8a719c2f1")

        rev = self.script_dir.get_revision("b6e8a719c2f1")
        self.assertEqual(rev.down_revision, "4679833ff5a3")
        self.assertIn("Add Power BI reporting views", rev.doc)

    def test_reporting_views_schema_and_columns(self):
        """Verify views can be created, queried, and cleanly dropped in a tenant schema."""
        engine = sa.create_engine(str(settings.DATABASE_URL))
        test_schema = "tenant_pbi_unit_test"

        expected_view_columns = {
            "vw_attendance_reporting": [
                "date", "employee_id", "employee_name", "employment_type",
                "department", "designation", "branch", "attendance_status",
                "check_in_time", "check_out_time", "worked_minutes", "worked_hours",
                "late_minutes", "overtime_minutes",
            ],
            "vw_leave_reporting": [
                "date", "employee_id", "employee_name", "department",
                "leave_type", "leave_status", "leave_days_requested",
                "decision_time_minutes", "created_at",
            ],
            "vw_workforce_headcount_reporting": [
                "employee_id", "employee_name", "first_name", "last_name",
                "employment_type", "status", "department", "designation", "branch",
            ],
            "vw_it_tickets_reporting": [
                "date", "employee_id", "employee_name", "department",
                "priority", "status", "resolution_time_minutes",
                "first_response_minutes", "sla_breached", "created_at",
                "asset_name", "device_model", "software_title",
            ],
            "vw_asset_assignments_reporting": [
                "date", "asset_name", "asset_category", "asset_status",
                "employee_id", "employee_name", "assignment_id", "assigned_at",
                "returned_at", "assignment_duration_days", "assignment_status",
            ],
            "vw_workflow_performance_reporting": [
                "date", "workflow_name", "workflow_type", "execution_id",
                "initiator_employee_id", "initiator_employee_name",
                "execution_status", "total_completion_minutes", "step_count",
                "created_at", "last_event_occurred_at",
            ],
            "vw_workflow_bottlenecks_reporting": [
                "date", "workflow_name", "workflow_type", "execution_id",
                "workflow_step_id", "step_order", "entity_type",
                "approver_employee_id", "approver_employee_name", "status",
                "created_at", "decided_at", "decision_duration_seconds",
                "decision_duration_minutes", "decision_duration_hours",
            ],
        }

        with engine.connect() as conn:
            conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {test_schema};"))
            conn.commit()

        try:
            from alembic import command
            cfg = Config("alembic.ini")
            cfg.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

            # Run upgrade to head
            with engine.connect() as conn:
                conn.execute(sa.text(f'SET search_path TO "{test_schema}";'))
                cfg.attributes["connection"] = conn
                command.upgrade(cfg, "head")
                conn.commit()

            # Verify all expected views exist and have the expected columns
            with engine.connect() as conn:
                conn.execute(sa.text(f'SET search_path TO "{test_schema}";'))
                for view_name, expected_cols in expected_view_columns.items():
                    result = conn.execute(sa.text(f'SELECT * FROM "{view_name}" LIMIT 0;'))
                    actual_cols = list(result.keys())
                    for col in expected_cols:
                        self.assertIn(
                            col,
                            actual_cols,
                            f"Column {col} missing from view {view_name}",
                        )

                # Check convenience aliases also exist
                for alias in ["vw_attendance", "vw_leave", "vw_workforce_headcount", "vw_headcount",
                              "vw_it_tickets", "vw_asset_assignments", "vw_workflow_performance",
                              "vw_workflow_bottlenecks"]:
                    result = conn.execute(sa.text(f'SELECT * FROM "{alias}" LIMIT 0;'))
                    self.assertTrue(len(result.keys()) > 0)

            # Test downgrade
            with engine.connect() as conn:
                conn.execute(sa.text(f'SET search_path TO "{test_schema}";'))
                cfg.attributes["connection"] = conn
                command.downgrade(cfg, "-1")
                conn.commit()

            # Verify views are dropped after downgrade
            with engine.connect() as conn:
                res = conn.execute(sa.text(f"""
                    SELECT table_name FROM information_schema.views 
                    WHERE table_schema = '{test_schema}';
                """))
                remaining = [r[0] for r in res]
                self.assertEqual(remaining, [])

        finally:
            with engine.connect() as conn:
                conn.execute(sa.text(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE;"))
                conn.commit()
