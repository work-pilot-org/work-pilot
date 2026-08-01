from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ==================================================================
# Leave Type Config Schemas
# ==================================================================

class LeaveTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = None
    days_per_year: int = Field(..., ge=0)
    is_paid: bool = True
    carry_forward: bool = False


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None
    days_per_year: int | None = Field(None, ge=0)
    is_paid: bool | None = None
    carry_forward: bool | None = None
    is_active: bool | None = None


class LeaveTypeResponse(LeaveTypeBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LeaveTypeListResponse(BaseModel):
    leave_types: list[LeaveTypeResponse]


# ==================================================================
# Enums
# ==================================================================

class LeaveType(str, Enum):
    CASUAL = "CASUAL"
    SICK = "SICK"
    EARNED = "EARNED"
    MATERNITY = "MATERNITY"
    PATERNITY = "PATERNITY"
    COMP_OFF = "COMP_OFF"
    UNPAID = "UNPAID"
    OTHER = "OTHER"


class LeaveStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


# ==================================================================
# Leave Request Schemas
# ==================================================================

# ------------------------------------------------------------------
# Create
# ------------------------------------------------------------------

class LeaveRequestCreate(BaseModel):
    employee_id: UUID
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str = Field(..., min_length=5, max_length=1000)
    is_half_day: bool = False
    attachment_url: str | None = None
    emergency_contact: str | None = Field(None, max_length=100)

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, value, info):
        start = info.data.get("start_date")
        if start and value < start:
            raise ValueError("End date cannot be before start date.")
        return value


# ------------------------------------------------------------------
# Update
# ------------------------------------------------------------------

class LeaveRequestUpdate(BaseModel):
    leave_type: LeaveType | None = None
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = Field(None, min_length=5, max_length=1000)
    is_half_day: bool | None = None
    attachment_url: str | None = None
    emergency_contact: str | None = Field(None, max_length=100)

class LeaveRequestStatusUpdate(BaseModel):
    status: LeaveStatus


# ------------------------------------------------------------------
# Response
# ------------------------------------------------------------------

class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: UUID
    leave_type: LeaveType
    start_date: date
    end_date: date
    total_days: int
    reason: str
    is_half_day: bool
    attachment_url: str | None
    emergency_contact: str | None
    status: LeaveStatus
    workflow_instance_id: UUID | None
    created_at: datetime
    updated_at: datetime


# ------------------------------------------------------------------
# List Response
# ------------------------------------------------------------------

class LeaveRequestListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: UUID
    leave_type: LeaveType
    start_date: date
    end_date: date
    total_days: int
    status: LeaveStatus


# ==================================================================
# Leave Balance Schemas
# ==================================================================

# ------------------------------------------------------------------
# Allocate (Create)
# ------------------------------------------------------------------

class LeaveBalanceCreate(BaseModel):
    """Payload to allocate a leave balance entry for an employee."""

    employee_id: UUID
    leave_type: LeaveType
    year: int = Field(..., ge=2000, le=2100)
    allocated_days: Decimal = Field(..., ge=0, decimal_places=1)
    carried_forward_days: Decimal = Field(default=Decimal("0.0"), ge=0, decimal_places=1)
    notes: str | None = None


# ------------------------------------------------------------------
# Update
# ------------------------------------------------------------------

class LeaveBalanceUpdate(BaseModel):
    """Payload to update an existing leave balance record."""

    allocated_days: Decimal | None = Field(None, ge=0, decimal_places=1)
    used_days: Decimal | None = Field(None, ge=0, decimal_places=1)
    carried_forward_days: Decimal | None = Field(None, ge=0, decimal_places=1)
    notes: str | None = None


# ------------------------------------------------------------------
# Response
# ------------------------------------------------------------------

class LeaveBalanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: UUID
    leave_type: LeaveType
    year: int
    allocated_days: Decimal
    used_days: Decimal
    carried_forward_days: Decimal
    remaining_days: Decimal  # computed field — set by service
    notes: str | None
    created_at: datetime
    updated_at: datetime


# ==================================================================
# Employee Leave Endpoint Schemas
# ==================================================================

class LeaveBalanceSummaryItem(BaseModel):
    """Per-leave-type breakdown used in balance and summary responses."""

    model_config = ConfigDict(from_attributes=True)

    leave_type: LeaveType
    year: int
    allocated_days: Decimal
    used_days: Decimal
    carried_forward_days: Decimal
    remaining_days: Decimal


class EmployeeLeaveBalanceResponse(BaseModel):
    """Response for GET /employees/{employee_id}/leave-balance."""

    employee_id: UUID
    balances: list[LeaveBalanceSummaryItem]


class LeaveSummaryItem(BaseModel):
    """Per-leave-type summary row combining requests + balance."""

    leave_type: LeaveType
    year: int
    total_requested_days: int
    approved_days: int
    pending_days: int
    rejected_days: int
    allocated_days: Decimal
    used_days: Decimal
    remaining_days: Decimal


class EmployeeLeaveSummaryResponse(BaseModel):
    """Response for GET /employees/{employee_id}/leave-summary."""

    employee_id: UUID
    summary: list[LeaveSummaryItem]


# ==================================================================
# Holiday Schemas
# ==================================================================

class HolidayCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    date: date
    is_optional: bool = False


class HolidayResponse(HolidayCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime


# ==================================================================
# Leave Report Schemas
# ==================================================================

class LeaveReportItem(BaseModel):
    """Aggregate stats for a specific leave type."""
    leave_type: LeaveType
    total_requested: int
    total_approved: int
    total_pending: int
    total_rejected: int


class OrganizationLeaveReportResponse(BaseModel):
    """Organization-wide leave report."""
    start_date: date | None = None
    end_date: date | None = None
    total_employees_on_leave: int
    report_items: list[LeaveReportItem]


class MonthlyLeaveReportItem(BaseModel):
    year: int
    month: int
    report_items: list[LeaveReportItem]


class MonthlyLeaveReportResponse(BaseModel):
    """Monthly leave report."""
    reports: list[MonthlyLeaveReportItem]


class DepartmentLeaveReportResponse(BaseModel):
    """Department-wise leave report."""
    department_id: UUID
    start_date: date | None = None
    end_date: date | None = None
    total_employees_on_leave: int
    report_items: list[LeaveReportItem]


# ==================================================================
# Leave Calendar Schemas
# ==================================================================

class EventType(str, Enum):
    LEAVE = "LEAVE"
    HOLIDAY = "HOLIDAY"


class CalendarEvent(BaseModel):
    """Unified event schema for the leave calendar."""
    id: UUID
    title: str
    date: date
    event_type: EventType
    # For LEAVE events
    employee_id: UUID | None = None
    leave_status: LeaveStatus | None = None
    # For HOLIDAY events
    is_optional_holiday: bool | None = None