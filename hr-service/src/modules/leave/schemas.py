from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import Enum

from datetime import date, datetime
from uuid import UUID


# ==================================================================
# Leave Type Config Schemas
# ==================================================================

class LeaveTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    days_per_year: int = Field(..., ge=0)
    is_paid: bool = True
    carry_forward: bool = False


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    days_per_year: Optional[int] = Field(None, ge=0)
    is_paid: Optional[bool] = None
    carry_forward: Optional[bool] = None
    is_active: Optional[bool] = None


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
    attachment_url: Optional[str] = None
    emergency_contact: Optional[str] = Field(None, max_length=100)

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
    leave_type: Optional[LeaveType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = Field(None, min_length=5, max_length=1000)
    is_half_day: Optional[bool] = None
    attachment_url: Optional[str] = None
    emergency_contact: Optional[str] = Field(None, max_length=100)


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
    attachment_url: Optional[str]
    emergency_contact: Optional[str]
    status: LeaveStatus
    workflow_instance_id: Optional[UUID]
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
    notes: Optional[str] = None


# ------------------------------------------------------------------
# Update
# ------------------------------------------------------------------

class LeaveBalanceUpdate(BaseModel):
    """Payload to update an existing leave balance record."""

    allocated_days: Optional[Decimal] = Field(None, ge=0, decimal_places=1)
    used_days: Optional[Decimal] = Field(None, ge=0, decimal_places=1)
    carried_forward_days: Optional[Decimal] = Field(None, ge=0, decimal_places=1)
    notes: Optional[str] = None


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
    notes: Optional[str]
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
    start_date: Optional[date] = None
    end_date: Optional[date] = None
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
    start_date: Optional[date] = None
    end_date: Optional[date] = None
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
    employee_id: Optional[UUID] = None
    leave_status: Optional[LeaveStatus] = None
    # For HOLIDAY events
    is_optional_holiday: Optional[bool] = None