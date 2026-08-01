"""
Leave tools for the HR Agent.
"""

from __future__ import annotations

from uuid import UUID

from modules.hr.client import hr_client
from modules.hr.registry import hr_tool_registry
from modules.hr.schemas import (
    CreateLeaveTypeToolInput,
    UpdateLeaveTypeToolInput,
    CreateLeaveToolInput,
    UpdateLeaveToolInput,
    UpdateLeaveToolInputStatus,
    CreateLeaveBalanceToolInput,
    UpdateLeaveBalanceToolInput,
    CreateHolidayToolInput,
)


# ==========================================================
# Leave Types
# ==========================================================

async def create_leave_type(
    payload: CreateLeaveTypeToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_leave_type(
        payload=payload.model_dump(mode="json"),
    )


async def get_leave_types(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_types()


async def get_leave_type(
    leave_type_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_type(
        leave_type_id=leave_type_id,
    )


async def update_leave_type(
    leave_type_id: int,
    payload: UpdateLeaveTypeToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_leave_type(
        leave_type_id=leave_type_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_leave_type(
    leave_type_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_leave_type(
        leave_type_id=leave_type_id,
    )


# ==========================================================
# Leave Requests
# ==========================================================

async def create_leave_request(
    payload: CreateLeaveToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_leave_request(
        payload=payload.model_dump(mode="json"),
    )


async def get_all_leave_requests(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_all_leave_requests()


async def get_leave_request(
    leave_request_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_request(
        leave_request_id=str(leave_request_id),
    )


async def update_leave_request(
    leave_request_id: UUID,
    payload: UpdateLeaveToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_leave_request(
        leave_request_id=str(leave_request_id),
        payload=payload.model_dump(exclude_unset=True),
    )


async def update_leave_request_status(
    leave_request_id: UUID,
    payload: UpdateLeaveToolInputStatus,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_leave_request_status(
        leave_request_id=str(leave_request_id),
        payload=payload.model_dump(),
    )


async def cancel_leave_request(
    leave_request_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.cancel_leave_request(
        leave_request_id=str(leave_request_id),
    )


# ==========================================================
# Employee Leave
# ==========================================================

async def get_employee_leave_requests(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee_leave_requests(
        employee_id=str(employee_id),
    )


async def get_employee_leave_balance(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee_leave_balance(
        employee_id=str(employee_id),
    )


async def get_employee_leave_summary(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee_leave_summary(
        employee_id=str(employee_id),
    )


# ==========================================================
# Leave Balance
# ==========================================================

async def create_leave_balance(
    payload: CreateLeaveBalanceToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_leave_balance(
        payload=payload.model_dump(mode="json"),
    )


async def get_all_leave_balances(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_all_leave_balances()


async def get_leave_balance(
    balance_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_balance(
        balance_id=str(balance_id),
    )


async def update_leave_balance(
    balance_id: UUID,
    payload: UpdateLeaveBalanceToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_leave_balance(
        balance_id=str(balance_id),
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_leave_balance(
    balance_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_leave_balance(
        balance_id=str(balance_id),
    )


# ==========================================================
# Reports
# ==========================================================

async def organization_leave_report(
    headers: dict[str, str] | None = None,
):
    return await hr_client.organization_leave_report()


async def monthly_leave_report(
    year: int,
    month: int | None = None,
    headers: dict[str, str] | None = None,
):
    return await hr_client.monthly_leave_report(
        year=year,
        month=month,
    )


async def department_leave_report(
    department_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.department_leave_report(
        department_id=str(department_id),
    )


async def leave_calendar(
    headers: dict[str, str] | None = None,
):
    return await hr_client.leave_calendar()


# ==========================================================
# Holidays
# ==========================================================

async def create_holiday(
    payload: CreateHolidayToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_holiday(
        payload=payload.model_dump(mode="json"),
    )


async def get_holidays(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_holidays()


async def delete_holiday(
    holiday_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_holiday(
        holiday_id=str(holiday_id),
    )


# ==========================================================
# Register Tools
# ==========================================================

hr_tool_registry.register("create_leave_type", create_leave_type)
hr_tool_registry.register("get_leave_types", get_leave_types)
hr_tool_registry.register("get_leave_type", get_leave_type)
hr_tool_registry.register("update_leave_type", update_leave_type)
hr_tool_registry.register("delete_leave_type", delete_leave_type)

hr_tool_registry.register("create_leave_request", create_leave_request)
hr_tool_registry.register("get_all_leave_requests", get_all_leave_requests)
hr_tool_registry.register("get_leave_request", get_leave_request)
hr_tool_registry.register("update_leave_request", update_leave_request)
hr_tool_registry.register("update_leave_request_status", update_leave_request_status)
hr_tool_registry.register("cancel_leave_request", cancel_leave_request)

hr_tool_registry.register("get_employee_leave_requests", get_employee_leave_requests)
hr_tool_registry.register("get_employee_leave_balance", get_employee_leave_balance)
hr_tool_registry.register("get_employee_leave_summary", get_employee_leave_summary)

hr_tool_registry.register("create_leave_balance", create_leave_balance)
hr_tool_registry.register("get_all_leave_balances", get_all_leave_balances)
hr_tool_registry.register("get_leave_balance", get_leave_balance)
hr_tool_registry.register("update_leave_balance", update_leave_balance)
hr_tool_registry.register("delete_leave_balance", delete_leave_balance)

hr_tool_registry.register("organization_leave_report", organization_leave_report)
hr_tool_registry.register("monthly_leave_report", monthly_leave_report)
hr_tool_registry.register("department_leave_report", department_leave_report)
hr_tool_registry.register("leave_calendar", leave_calendar)

hr_tool_registry.register("create_holiday", create_holiday)
hr_tool_registry.register("get_holidays", get_holidays)
hr_tool_registry.register("delete_holiday", delete_holiday)