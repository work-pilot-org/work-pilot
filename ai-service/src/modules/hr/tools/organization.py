"""
Organization tools for the HR Agent.
"""

from __future__ import annotations

from modules.hr.client import hr_client
from modules.hr.registry import hr_tool_registry
from modules.hr.schemas import (
    CreateDepartmentToolInput,
    UpdateDepartmentToolInput,
    CreateDesignationToolInput,
    UpdateDesignationToolInput,
    CreateBranchToolInput,
    UpdateBranchToolInput,
    CreateShiftToolInput,
    UpdateShiftToolInput,
)

# ==========================================================
# Department
# ==========================================================

async def create_department(
    payload: CreateDepartmentToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_department(
        payload=payload.model_dump(mode="json"),
    )


async def get_departments(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_departments()


async def update_department(
    department_id: int,
    payload: UpdateDepartmentToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_department(
        department_id=department_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_department(
    department_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_department(
        department_id=department_id,
    )


# ==========================================================
# Designation
# ==========================================================

async def create_designation(
    payload: CreateDesignationToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_designation(
        payload=payload.model_dump(mode="json"),
    )


async def get_designations(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_designations()


async def update_designation(
    designation_id: int,
    payload: UpdateDesignationToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_designation(
        designation_id=designation_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_designation(
    designation_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_designation(
        designation_id=designation_id,
    )


# ==========================================================
# Branch
# ==========================================================

async def create_branch(
    payload: CreateBranchToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_branch(
        payload=payload.model_dump(mode="json"),
    )


async def get_branches(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_branches()


async def update_branch(
    branch_id: int,
    payload: UpdateBranchToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_branch(
        branch_id=branch_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_branch(
    branch_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_branch(
        branch_id=branch_id,
    )


# ==========================================================
# Shift
# ==========================================================

async def create_shift(
    payload: CreateShiftToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_shift(
        payload=payload.model_dump(mode="json"),
    )


async def get_shifts(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_shifts()


async def update_shift(
    shift_id: int,
    payload: UpdateShiftToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_shift(
        shift_id=shift_id,
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_shift(
    shift_id: int,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_shift(
        shift_id=shift_id,
    )


# ==========================================================
# Register Tools
# ==========================================================

hr_tool_registry.register(
    "create_department",
    create_department,
)
hr_tool_registry.register(
    "get_departments",
    get_departments,
)
hr_tool_registry.register(
    "update_department",
    update_department,
)
hr_tool_registry.register(
    "delete_department",
    delete_department,
)

hr_tool_registry.register(
    "create_designation",
    create_designation,
)
hr_tool_registry.register(
    "get_designations",
    get_designations,
)
hr_tool_registry.register(
    "update_designation",
    update_designation,
)
hr_tool_registry.register(
    "delete_designation",
    delete_designation,
)

hr_tool_registry.register(
    "create_branch",
    create_branch,
)
hr_tool_registry.register(
    "get_branches",
    get_branches,
)
hr_tool_registry.register(
    "update_branch",
    update_branch,
)
hr_tool_registry.register(
    "delete_branch",
    delete_branch,
)

hr_tool_registry.register(
    "create_shift",
    create_shift,
)
hr_tool_registry.register(
    "get_shifts",
    get_shifts,
)
hr_tool_registry.register(
    "update_shift",
    update_shift,
)
hr_tool_registry.register(
    "delete_shift",
    delete_shift,
)