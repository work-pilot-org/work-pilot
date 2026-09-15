"""Add Power BI reporting views

Revision ID: b6e8a719c2f1
Revises: 4679833ff5a3
Create Date: 2026-09-09 18:50:00.000000

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b6e8a719c2f1'
down_revision: str | Sequence[str] | None = '4679833ff5a3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Attendance Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_attendance_reporting AS
    SELECT
        d.date AS date,
        e.employee_id AS employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS employee_name,
        e.employment_type AS employment_type,
        dept.name AS department,
        des.name AS designation,
        b.name AS branch,
        fa.attendance_status AS attendance_status,
        fa.check_in_time AS check_in_time,
        fa.check_out_time AS check_out_time,
        fa.worked_minutes AS worked_minutes,
        ROUND(fa.worked_minutes::numeric / 60.0, 2) AS worked_hours,
        fa.late_minutes AS late_minutes,
        fa.overtime_minutes AS overtime_minutes
    FROM fact_attendance fa
    LEFT JOIN dim_date d ON fa.date_key = d.id
    LEFT JOIN dim_employee e ON fa.employee_key = e.id
    LEFT JOIN dim_department dept ON fa.department_key = dept.id
    LEFT JOIN dim_designation des ON fa.designation_key = des.id
    LEFT JOIN dim_branch b ON fa.branch_key = b.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_attendance AS
    SELECT * FROM vw_attendance_reporting;
    """)

    # 2. Leave Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_leave_reporting AS
    SELECT
        d.date AS date,
        e.employee_id AS employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS employee_name,
        dept.name AS department,
        fl.leave_type AS leave_type,
        fl.leave_status AS leave_status,
        fl.leave_days_requested AS leave_days_requested,
        fl.decision_time_minutes AS decision_time_minutes,
        fl.created_at AS created_at
    FROM fact_leave fl
    LEFT JOIN dim_date d ON fl.date_key = d.id
    LEFT JOIN dim_employee e ON fl.employee_key = e.id
    LEFT JOIN dim_department dept ON fl.department_key = dept.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_leave AS
    SELECT * FROM vw_leave_reporting;
    """)

    # 3. Headcount / Workforce Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_workforce_headcount_reporting AS
    SELECT
        e.employee_id AS employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS employee_name,
        e.first_name AS first_name,
        e.last_name AS last_name,
        e.employment_type AS employment_type,
        e.status AS status,
        COALESCE(dept.name, dept_leave.name) AS department,
        des.name AS designation,
        b.name AS branch
    FROM dim_employee e
    LEFT JOIN LATERAL (
        SELECT fa.department_key, fa.designation_key, fa.branch_key
        FROM fact_attendance fa
        WHERE fa.employee_key = e.id
        ORDER BY fa.date_key DESC, fa.id DESC
        LIMIT 1
    ) latest_att ON TRUE
    LEFT JOIN dim_department dept ON latest_att.department_key = dept.id
    LEFT JOIN dim_designation des ON latest_att.designation_key = des.id
    LEFT JOIN dim_branch b ON latest_att.branch_key = b.id
    LEFT JOIN LATERAL (
        SELECT fl.department_key
        FROM fact_leave fl
        WHERE fl.employee_key = e.id
        ORDER BY fl.date_key DESC, fl.id DESC
        LIMIT 1
    ) latest_leave ON TRUE
    LEFT JOIN dim_department dept_leave ON latest_leave.department_key = dept_leave.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_workforce_headcount AS
    SELECT * FROM vw_workforce_headcount_reporting;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_headcount AS
    SELECT * FROM vw_workforce_headcount_reporting;
    """)

    # 4. IT Tickets Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_it_tickets_reporting AS
    SELECT
        d.date AS date,
        e.employee_id AS employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS employee_name,
        dept.name AS department,
        t.priority AS priority,
        t.status AS status,
        t.resolution_time_minutes AS resolution_time_minutes,
        t.first_response_minutes AS first_response_minutes,
        t.sla_breached AS sla_breached,
        t.created_at AS created_at,
        a.name AS asset_name,
        dev.model AS device_model,
        soft.title AS software_title
    FROM fact_it_ticket t
    LEFT JOIN dim_date d ON t.date_key = d.id
    LEFT JOIN dim_employee e ON t.employee_key = e.id
    LEFT JOIN dim_department dept ON t.department_key = dept.id
    LEFT JOIN dim_asset a ON t.asset_key = a.id
    LEFT JOIN dim_device dev ON t.device_key = dev.id
    LEFT JOIN dim_software soft ON t.software_key = soft.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_it_tickets AS
    SELECT * FROM vw_it_tickets_reporting;
    """)

    # 5. Asset Assignments Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_asset_assignments_reporting AS
    SELECT
        d.date AS date,
        a.name AS asset_name,
        a.category AS asset_category,
        a.status AS asset_status,
        e.employee_id AS employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS employee_name,
        fa.assignment_id AS assignment_id,
        fa.assigned_at AS assigned_at,
        fa.returned_at AS returned_at,
        fa.assignment_duration_days AS assignment_duration_days,
        fa.assignment_status AS assignment_status
    FROM fact_asset_assignment fa
    LEFT JOIN dim_date d ON fa.date_key = d.id
    LEFT JOIN dim_asset a ON fa.asset_key = a.id
    LEFT JOIN dim_employee e ON fa.employee_key = e.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_asset_assignments AS
    SELECT * FROM vw_asset_assignments_reporting;
    """)

    # 6. Workflow Performance Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_workflow_performance_reporting AS
    SELECT
        d.date AS date,
        w.name AS workflow_name,
        w.workflow_type AS workflow_type,
        we.execution_id AS execution_id,
        e.employee_id AS initiator_employee_id,
        TRIM(CONCAT(e.first_name, ' ', e.last_name)) AS initiator_employee_name,
        we.execution_status AS execution_status,
        we.total_completion_minutes AS total_completion_minutes,
        we.step_count AS step_count,
        we.created_at AS created_at,
        we.last_event_occurred_at AS last_event_occurred_at
    FROM fact_workflow_execution we
    LEFT JOIN dim_date d ON we.date_key = d.id
    LEFT JOIN dim_workflow w ON we.workflow_key = w.id
    LEFT JOIN dim_employee e ON we.employee_key = e.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_workflow_performance AS
    SELECT * FROM vw_workflow_performance_reporting;
    """)

    # 7. Workflow Bottlenecks Reporting View
    op.execute("""
    CREATE OR REPLACE VIEW vw_workflow_bottlenecks_reporting AS
    SELECT
        d.date AS date,
        w.name AS workflow_name,
        w.workflow_type AS workflow_type,
        ws.execution_id AS execution_id,
        ws.workflow_step_id AS workflow_step_id,
        ws.step_order AS step_order,
        ws.entity_type AS entity_type,
        app.employee_id AS approver_employee_id,
        TRIM(CONCAT(app.first_name, ' ', app.last_name)) AS approver_employee_name,
        ws.status AS status,
        ws.created_at AS created_at,
        ws.decided_at AS decided_at,
        ws.decision_duration_seconds AS decision_duration_seconds,
        ROUND(ws.decision_duration_seconds::numeric / 60.0, 2) AS decision_duration_minutes,
        ROUND(ws.decision_duration_seconds::numeric / 3600.0, 2) AS decision_duration_hours
    FROM fact_workflow_step ws
    LEFT JOIN dim_date d ON ws.date_key = d.id
    LEFT JOIN dim_workflow w ON ws.workflow_key = w.id
    LEFT JOIN dim_employee app ON ws.approver_key = app.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW vw_workflow_bottlenecks AS
    SELECT * FROM vw_workflow_bottlenecks_reporting;
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS vw_workflow_bottlenecks CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_workflow_bottlenecks_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_workflow_performance CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_workflow_performance_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_asset_assignments CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_asset_assignments_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_it_tickets CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_it_tickets_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_headcount CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_workforce_headcount CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_workforce_headcount_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_leave CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_leave_reporting CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_attendance CASCADE;")
    op.execute("DROP VIEW IF EXISTS vw_attendance_reporting CASCADE;")
