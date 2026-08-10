"""
Attendance tools for the HR Agent.
"""

from __future__ import annotations

from datetime import date
from uuid import UUID

from modules.hr.client import hr_client
from modules.hr.registry import hr_tool_registry
from modules.hr.schemas import (
    CheckInToolInput,
    CheckOutToolInput,
    CreateAttendanceToolInput,
    UpdateAttendanceToolInput,
    UpdateAttendanceStatusToolInput,
)


# ==========================================================
# Check In / Check Out
# ==========================================================

async def check_in(
    payload: CheckInToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.check_in(
        payload=payload.model_dump(mode="json"),
    )


async def check_out(
    payload: CheckOutToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.check_out(
        payload=payload.model_dump(mode="json"),
    )


# ==========================================================
# Attendance CRUD
# ==========================================================

async def create_attendance(
    payload: CreateAttendanceToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_attendance(
        payload=payload.model_dump(mode="json"),
    )


async def get_all_attendance(
    skip: int = 0,
    limit: int = 100,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_all_attendance(
        skip=skip,
        limit=limit,
    )


async def get_attendance(
    attendance_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_attendance(
        attendance_id=attendance_id,
    )


async def update_attendance(
    attendance_id: int,
    payload: UpdateAttendanceToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_attendance(
        attendance_id=attendance_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_attendance(
    attendance_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_attendance(
        attendance_id=attendance_id,
    )


# ==========================================================
# Employee Attendance
# ==========================================================

async def get_employee_attendance(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee_attendance(
        employee_id=str(employee_id),
    )


async def attendance_summary(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.attendance_summary(
        employee_id=str(employee_id),
    )


# ==========================================================
# Attendance Queries
# ==========================================================

async def get_attendance_by_date(
    attendance_date: date,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_attendance_by_date(
        attendance_date=attendance_date.isoformat(),
    )


async def today_attendance(
    headers: dict[str, str] | None = None,
):
    return await hr_client.today_attendance(headers=headers)


async def get_active_attendance(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_active_attendance(headers=headers)


# ==========================================================
# Attendance Status
# ==========================================================

async def update_attendance_status(
    attendance_id: int,
    payload: UpdateAttendanceStatusToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_attendance_status(
        attendance_id=attendance_id,
        payload=payload.model_dump(),
    )


# ==========================================================
# Reports
# ==========================================================

async def monthly_report(
    year: int,
    month: int | None = None,
    headers: dict[str, str] | None = None,
):
    return await hr_client.monthly_report(
        year=year,
        month=month,
    )


async def export_attendance(
    month: int,
    year: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.export_attendance(
        month=month,
        year=year,
    )


# ==========================================================
# Register Tools
# ==========================================================

hr_tool_registry.register("check_in", check_in)
hr_tool_registry.register("check_out", check_out)

hr_tool_registry.register("create_attendance", create_attendance)
hr_tool_registry.register("get_all_attendance", get_all_attendance)
hr_tool_registry.register("get_attendance", get_attendance)
hr_tool_registry.register("update_attendance", update_attendance)
hr_tool_registry.register("delete_attendance", delete_attendance)

hr_tool_registry.register(
    "get_employee_attendance",
    get_employee_attendance,
)
hr_tool_registry.register(
    "attendance_summary",
    attendance_summary,
)

hr_tool_registry.register(
    "get_attendance_by_date",
    get_attendance_by_date,
)
hr_tool_registry.register(
    "today_attendance",
    today_attendance,
)
hr_tool_registry.register(
    "get_active_attendance",
    get_active_attendance,
)

hr_tool_registry.register(
    "update_attendance_status",
    update_attendance_status,
)

hr_tool_registry.register(
    "monthly_report",
    monthly_report,
)
hr_tool_registry.register(
    "export_attendance",
    export_attendance,
)