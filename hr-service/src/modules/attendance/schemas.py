from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.modules.attendance.models import AttendanceStatus


# =====================================================
# Base Schema
# =====================================================

class AttendanceBase(BaseModel):
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: AttendanceStatus = AttendanceStatus.PRESENT
    remarks: Optional[str] = Field(
        default=None,
        max_length=500,
    )


# =====================================================
# Create Attendance
# POST /attendance
# =====================================================

class AttendanceCreate(AttendanceBase):
    employee_id: UUID


# =====================================================
# Update Attendance
# PUT /attendance/{attendance_id}
# =====================================================

class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[AttendanceStatus] = None
    remarks: Optional[str] = Field(
        default=None,
        max_length=500,
    )


# =====================================================
# Check In
# POST /attendance/check-in
# =====================================================

class AttendanceCheckIn(BaseModel):
    employee_id: UUID


# =====================================================
# Check Out
# POST /attendance/check-out
# =====================================================

class AttendanceCheckOut(BaseModel):
    employee_id: UUID


# =====================================================
# Update Status
# PATCH /attendance/{attendance_id}/status
# =====================================================

class AttendanceStatusUpdate(BaseModel):
    status: AttendanceStatus


# =====================================================
# Attendance Response
# =====================================================

class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: UUID

    attendance_date: date

    check_in: Optional[time]
    check_out: Optional[time]

    status: AttendanceStatus

    working_minutes: int
    overtime_minutes: int

    remarks: Optional[str]

    created_at: datetime
    updated_at: datetime


# =====================================================
# Employee Attendance Summary Response
# GET /attendance/employee/{employee_id}/summary
# =====================================================

class AttendanceSummaryResponse(BaseModel):
    employee_id: UUID

    total_days: int
    present_days: int
    absent_days: int
    half_days: int
    late_days: int

    total_working_minutes: int
    total_overtime_minutes: int


# =====================================================
# Monthly Attendance Report Response
# GET /attendance/report/monthly
# =====================================================

class MonthlyAttendanceReportResponse(BaseModel):
    month: int
    year: int

    total_days: int
    present_days: int
    absent_days: int
    half_days: int
    late_days: int

    total_working_minutes: int
    total_overtime_minutes: int

    records: list[AttendanceResponse] = Field(default_factory=list)


# =====================================================
# Export Response
# GET /attendance/export
# =====================================================

class AttendanceExportResponse(BaseModel):
    message: str
    file_path: str
