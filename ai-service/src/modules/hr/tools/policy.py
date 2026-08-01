"""
Policy tools for the HR Agent.
"""

from __future__ import annotations

from modules.hr.client import hr_client
from modules.hr.registry import hr_tool_registry
from modules.hr.schemas import (
    CreateLeavePolicyToolInput,
    UpdateLeavePolicyToolInput,
    CreateAttendancePolicyToolInput,
    UpdateAttendancePolicyToolInput,
    CreateShiftPolicyToolInput,
    UpdateShiftPolicyToolInput,
    CreateHolidayPolicyToolInput,
    UpdateHolidayPolicyToolInput,
    CreateProbationPolicyToolInput,
    UpdateProbationPolicyToolInput,
)

# ==========================================================
# Leave Policy
# ==========================================================

async def create_leave_policy(
    payload: CreateLeavePolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_leave_policy(
        payload=payload.model_dump(mode="json"),
    )


async def get_leave_policies(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_policies()


async def get_leave_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_leave_policy(policy_id)


async def update_leave_policy(
    policy_id: str,
    payload: UpdateLeavePolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_leave_policy(
        policy_id=policy_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_leave_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_leave_policy(policy_id)


# ==========================================================
# Attendance Policy
# ==========================================================

async def create_attendance_policy(
    payload: CreateAttendancePolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_attendance_policy(
        payload=payload.model_dump(mode="json"),
    )


async def get_attendance_policies(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_attendance_policies()


async def get_attendance_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_attendance_policy(policy_id)


async def update_attendance_policy(
    policy_id: str,
    payload: UpdateAttendancePolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_attendance_policy(
        policy_id=policy_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_attendance_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_attendance_policy(policy_id)


# ==========================================================
# Shift Policy
# ==========================================================

async def create_shift_policy(
    payload: CreateShiftPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_shift_policy(
        payload=payload.model_dump(mode="json"),
    )


async def get_shift_policies(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_shift_policies()


async def get_shift_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_shift_policy(policy_id)


async def update_shift_policy(
    policy_id: str,
    payload: UpdateShiftPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_shift_policy(
        policy_id=policy_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_shift_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_shift_policy(policy_id)


# ==========================================================
# Holiday Policy
# ==========================================================

async def create_holiday_policy(
    payload: CreateHolidayPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_holiday_policy(
        payload=payload.model_dump(mode="json"),
    )


async def get_holiday_policies(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_holiday_policies()


async def get_holiday_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_holiday_policy(policy_id)


async def update_holiday_policy(
    policy_id: str,
    payload: UpdateHolidayPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_holiday_policy(
        policy_id=policy_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_holiday_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_holiday_policy(policy_id)


# ==========================================================
# Probation Policy
# ==========================================================

async def create_probation_policy(
    payload: CreateProbationPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_probation_policy(
        payload=payload.model_dump(mode="json"),
    )


async def get_probation_policies(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_probation_policies()


async def get_probation_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_probation_policy(policy_id)


async def update_probation_policy(
    policy_id: str,
    payload: UpdateProbationPolicyToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_probation_policy(
        policy_id=policy_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_probation_policy(
    policy_id: str,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_probation_policy(policy_id)


# ==========================================================
# Register Tools
# ==========================================================

# Leave Policy
hr_tool_registry.register("create_leave_policy", create_leave_policy)
hr_tool_registry.register("get_leave_policies", get_leave_policies)
hr_tool_registry.register("get_leave_policy", get_leave_policy)
hr_tool_registry.register("update_leave_policy", update_leave_policy)
hr_tool_registry.register("delete_leave_policy", delete_leave_policy)

# Attendance Policy
hr_tool_registry.register("create_attendance_policy", create_attendance_policy)
hr_tool_registry.register("get_attendance_policies", get_attendance_policies)
hr_tool_registry.register("get_attendance_policy", get_attendance_policy)
hr_tool_registry.register("update_attendance_policy", update_attendance_policy)
hr_tool_registry.register("delete_attendance_policy", delete_attendance_policy)

# Shift Policy
hr_tool_registry.register("create_shift_policy", create_shift_policy)
hr_tool_registry.register("get_shift_policies", get_shift_policies)
hr_tool_registry.register("get_shift_policy", get_shift_policy)
hr_tool_registry.register("update_shift_policy", update_shift_policy)
hr_tool_registry.register("delete_shift_policy", delete_shift_policy)

# Holiday Policy
hr_tool_registry.register("create_holiday_policy", create_holiday_policy)
hr_tool_registry.register("get_holiday_policies", get_holiday_policies)
hr_tool_registry.register("get_holiday_policy", get_holiday_policy)
hr_tool_registry.register("update_holiday_policy", update_holiday_policy)
hr_tool_registry.register("delete_holiday_policy", delete_holiday_policy)

# Probation Policy
hr_tool_registry.register("create_probation_policy", create_probation_policy)
hr_tool_registry.register("get_probation_policies", get_probation_policies)
hr_tool_registry.register("get_probation_policy", get_probation_policy)
hr_tool_registry.register("update_probation_policy", update_probation_policy)
hr_tool_registry.register("delete_probation_policy", delete_probation_policy)