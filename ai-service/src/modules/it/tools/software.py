"""
Software tools for the IT Agent.
"""

from __future__ import annotations

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    CreateInstallationRequest,
    CreateInstallRequest,
    CreateSoftwareRequest,
    UpdateSoftwareRequest,
)

# ==========================================================
# Software Management
# ==========================================================

async def create_software(
    payload: CreateSoftwareRequest,
    headers: dict[str, str] | None = None,
):
    """
    Create a software record.
    """
    return await it_client.create_software(
        payload=payload,
        )


async def list_software(
    headers: dict[str, str] | None = None,
):
    """
    List all software.
    """
    return await it_client.list_software(
        )


async def get_software(
    software_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Get software details.
    """
    return await it_client.get_software(
        software_id=software_id,
        )


async def update_software(
    software_id: UUID,
    payload: UpdateSoftwareRequest,
    headers: dict[str, str] | None = None,
):
    """
    Update software details.
    """
    return await it_client.update_software(
        software_id=software_id,
        payload=payload,
        )


async def delete_software(
    software_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Delete software.
    """
    return await it_client.delete_software(
        software_id=software_id,
        )


# ==========================================================
# Installation
# ==========================================================

async def install_software(
    software_id: UUID,
    payload: CreateInstallRequest,
    headers: dict[str, str] | None = None,
):
    """
    Install software.
    """
    return await it_client.install_software(
        software_id=software_id,
        payload=payload,
        )


async def uninstall_software(
    install_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Uninstall software.
    """
    return await it_client.uninstall_software(
        install_id=install_id,
        )


async def list_device_installations(
    device_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    List software installed on a device.
    """
    return await it_client.list_device_installations(
        device_id=device_id,
        )


async def list_user_installations(
    user_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    List software assigned to a user.
    """
    return await it_client.list_user_installations(
        user_id=user_id,
        )


# ==========================================================
# Installation Requests
# ==========================================================

async def create_installation_request(
    payload: CreateInstallationRequest,
    headers: dict[str, str] | None = None,
):
    """
    Create a software installation request.
    """
    return await it_client.create_installation_request(
        payload=payload,
        )


async def list_installation_requests(
    headers: dict[str, str] | None = None,
):
    """
    List all installation requests.
    """
    return await it_client.list_installation_requests(
        )


async def get_installation_request(
    request_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Get installation request details.
    """
    return await it_client.get_installation_request(
        request_id=request_id,
        )


# ==========================================================
# Register Software Tools
# ==========================================================

tool_registry.register("create_software", create_software)
tool_registry.register("list_software", list_software)
tool_registry.register("get_software", get_software)
tool_registry.register("update_software", update_software)
tool_registry.register("delete_software", delete_software)

tool_registry.register("install_software", install_software)
tool_registry.register("uninstall_software", uninstall_software)

tool_registry.register(
    "list_device_installations",
    list_device_installations,
)
tool_registry.register(
    "list_user_installations",
    list_user_installations,
)

tool_registry.register(
    "create_installation_request",
    create_installation_request,
)
tool_registry.register(
    "list_installation_requests",
    list_installation_requests,
)
tool_registry.register(
    "get_installation_request",
    get_installation_request,
)