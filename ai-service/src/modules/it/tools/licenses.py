"""
License tools for the IT Agent.
"""

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    AssignLicenseRequest,
    CreateLicenseRequest,
    UpdateLicenseRequest,
)


async def create_license(payload: CreateLicenseRequest, headers=None):
    return await it_client.create_license(payload, headers)


async def list_licenses(headers=None):
    return await it_client.list_licenses(headers)


async def get_license(license_id: UUID, headers=None):
    return await it_client.get_license(license_id, headers)


async def update_license(
    license_id: UUID,
    payload: UpdateLicenseRequest,
    headers=None,
):
    return await it_client.update_license(
        license_id,
        payload,
        headers,
    )


async def delete_license(license_id: UUID, headers=None):
    return await it_client.delete_license(
        license_id,
        headers,
    )


async def assign_license(
    license_id: UUID,
    payload: AssignLicenseRequest,
    headers=None,
):
    return await it_client.assign_license(
        license_id,
        payload,
        headers,
    )


async def return_license(
    license_id: UUID,
    headers=None,
):
    return await it_client.return_license(
        license_id,
        headers,
    )


async def list_license_assignments(
    license_id: UUID,
    headers=None,
):
    return await it_client.list_license_assignments(
        license_id,
        headers,
    )


tool_registry.register("create_license", create_license)
tool_registry.register("list_licenses", list_licenses)
tool_registry.register("get_license", get_license)
tool_registry.register("update_license", update_license)
tool_registry.register("delete_license", delete_license)
tool_registry.register("assign_license", assign_license)
tool_registry.register("return_license", return_license)
tool_registry.register(
    "list_license_assignments",
    list_license_assignments,
)