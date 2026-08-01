"""
Employee tools for the HR Agent.
"""

from __future__ import annotations

from uuid import UUID

from modules.hr.client import hr_client
from modules.hr.registry import hr_tool_registry
from modules.hr.schemas import (
    CreateEmployeeToolInput,
    UpdateEmployeeToolInput,
    UpdateEmployeeProfileToolInput,
    UploadEmployeeDocumentToolInput,
)


# ==========================================================
# Employee
# ==========================================================

async def create_employee(
    payload: CreateEmployeeToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.create_employee(
        payload=payload.model_dump(mode="json"),
    )


async def get_all_employees(
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_all_employees()


async def get_employee(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee(
        employee_id=str(employee_id),
    )


async def update_employee(
    employee_id: UUID,
    payload: UpdateEmployeeToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_employee(
        employee_id=str(employee_id),
        payload=payload.model_dump(exclude_unset=True),
    )


async def delete_employee(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_employee(
        employee_id=str(employee_id),
    )


async def search_employee(
    keyword: str,
    page: int = 1,
    size: int = 10,
    headers: dict[str, str] | None = None,
):
    return await hr_client.search_employee(
        keyword=keyword,
        page=page,
        size=size,
    )


# ==========================================================
# Employee Profile
# ==========================================================

async def get_employee_profile(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_employee_profile(
        employee_id=str(employee_id),
    )


async def update_employee_profile(
    employee_id: UUID,
    payload: UpdateEmployeeProfileToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.update_employee_profile(
        employee_id=str(employee_id),
        payload=payload.model_dump(exclude_unset=True),
    )


# ==========================================================
# Employee Documents
# ==========================================================

async def upload_document(
    employee_id: UUID,
    payload: UploadEmployeeDocumentToolInput,
    headers: dict[str, str] | None = None,
):
    return await hr_client.upload_document(
        employee_id=str(employee_id),
        payload=payload.model_dump(mode="json"),
    )


async def get_documents(
    employee_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.get_documents(
        employee_id=str(employee_id),
    )


async def delete_document(
    employee_id: UUID,
    document_id: UUID,
    headers: dict[str, str] | None = None,
):
    return await hr_client.delete_document(
        employee_id=str(employee_id),
        document_id=str(document_id),
    )


# ==========================================================
# Register Tools
# ==========================================================

hr_tool_registry.register("create_employee", create_employee)
hr_tool_registry.register("get_all_employees", get_all_employees)
hr_tool_registry.register("get_employee", get_employee)
hr_tool_registry.register("update_employee", update_employee)
hr_tool_registry.register("delete_employee", delete_employee)
hr_tool_registry.register("search_employee", search_employee)

hr_tool_registry.register("get_employee_profile", get_employee_profile)
hr_tool_registry.register(
    "update_employee_profile",
    update_employee_profile,
)

hr_tool_registry.register("upload_document", upload_document)
hr_tool_registry.register("get_documents", get_documents)
hr_tool_registry.register("delete_document", delete_document)