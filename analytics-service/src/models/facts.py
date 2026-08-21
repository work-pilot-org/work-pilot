from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import TenantBase


class FactAttendance(TenantBase):
    __tablename__ = "fact_attendance"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys to Dimensions (Surrogate Keys)
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)
    department_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_department.id"), nullable=True)
    designation_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_designation.id"), nullable=True)
    branch_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_branch.id"), nullable=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    check_in_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    check_out_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Measures
    worked_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    late_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    overtime_minutes: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    attendance_status: Mapped[str] = mapped_column(String(50), nullable=False)


class FactLeave(TenantBase):
    __tablename__ = "fact_leave"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)
    department_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_department.id"), nullable=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Measures
    leave_days_requested: Mapped[int] = mapped_column(Integer, nullable=False)
    decision_time_minutes: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    leave_status: Mapped[str] = mapped_column(String(50), nullable=False)
    leave_type: Mapped[str] = mapped_column(String(100), nullable=False)


class FactITTicket(TenantBase):
    __tablename__ = "fact_it_ticket"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)
    department_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_department.id"), nullable=True)
    asset_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_asset.id"), nullable=True)
    device_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_device.id"), nullable=True)
    software_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_software.id"), nullable=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Measures
    resolution_time_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    first_response_minutes: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate / Boolean Dimensions
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    sla_breached: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class FactWorkflowExecution(TenantBase):
    __tablename__ = "fact_workflow_execution"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)
    workflow_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_workflow.id"), nullable=False, index=True)

    # Operational Traceability
    execution_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_event_occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("tenant_key", "execution_id", name="uq_tenant_execution"),)

    # Measures
    total_completion_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    step_count: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    execution_status: Mapped[str] = mapped_column(String(50), nullable=False)


class FactWorkflowStep(TenantBase):
    __tablename__ = "fact_workflow_step"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Composite Logical Uniqueness (Business Constraint)
    execution_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    workflow_step_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    workflow_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_workflow.id"), nullable=False, index=True)
    approver_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=True, index=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_event_occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("tenant_key", "execution_id", "workflow_step_id", name="uq_tenant_execution_step"),)

    # Flow details
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Bottleneck Metrics
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    decision_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class FactNotification(TenantBase):
    __tablename__ = "fact_notification"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Measures
    delivery_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class FactAIInteraction(TenantBase):
    __tablename__ = "fact_ai_interaction"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Measures
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate / Boolean Dimensions
    agent: Mapped[str] = mapped_column(String(100), nullable=False)
    intent: Mapped[str] = mapped_column(String(150), nullable=False)
    tool: Mapped[str] = mapped_column(String(150), nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class FactAssetAssignment(TenantBase):
    __tablename__ = "fact_asset_assignment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Business Identifier
    assignment_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)

    __table_args__ = (UniqueConstraint("tenant_key", "assignment_id", name="uq_tenant_assignment"),)

    # Foreign Keys
    tenant_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_tenant.id"), nullable=False, index=True)
    date_key: Mapped[int] = mapped_column(Integer, ForeignKey("dim_date.id"), nullable=False, index=True)
    asset_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_asset.id"), nullable=False, index=True)
    employee_key: Mapped[int] = mapped_column(BigInteger, ForeignKey("dim_employee.id"), nullable=False, index=True)

    # Operational Traceability
    source_event_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_event_occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Lifecycles & Measures
    assigned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    assignment_duration_days: Mapped[int] = mapped_column(Integer, nullable=True)

    # Degenerate Dimensions
    assignment_status: Mapped[str] = mapped_column(String(50), nullable=False)
