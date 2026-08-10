"""
Device tools for the IT Agent.
"""

from __future__ import annotations

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    AssignDeviceRequest,
    CreateDeviceRequest,
    CreateMaintenanceHistoryRequest,
    UpdateDeviceRequest,
)

# ==========================================================
# Device Tools
# ==========================================================

async def create_device(
    payload: CreateDeviceRequest,
    headers: dict[str, str] | None = None,
):
    """
    Create a new device.
    """
    return await it_client.create_device(
        payload=payload,
        )


async def list_devices(
    headers: dict[str, str] | None = None,
):
    """
    List all devices.
    """
    return await it_client.list_devices(
        )


async def get_device(
    device_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Retrieve a device by ID.
    """
    return await it_client.get_device(
        device_id=device_id,
        )


async def update_device(
    device_id: UUID,
    payload: UpdateDeviceRequest,
    headers: dict[str, str] | None = None,
):
    """
    Update a device.
    """
    return await it_client.update_device(
        device_id=device_id,
        payload=payload,
        )


async def delete_device(
    device_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Delete a device.
    """
    return await it_client.delete_device(
        device_id=device_id,
        )


async def assign_device(
    device_id: UUID,
    payload: AssignDeviceRequest,
    headers: dict[str, str] | None = None,
):
    """
    Assign a device to a user.
    """
    return await it_client.assign_device(
        device_id=device_id,
        payload=payload,
        )


async def return_device(
    device_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Return an assigned device.
    """
    return await it_client.return_device(
        device_id=device_id,
        )


async def add_maintenance_log(
    device_id: UUID,
    payload: CreateMaintenanceHistoryRequest,
    headers: dict[str, str] | None = None,
):
    """
    Add a maintenance log for a device.
    """
    return await it_client.add_maintenance_log(
        device_id=device_id,
        payload=payload,
        )


async def get_maintenance_history(
    device_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Retrieve maintenance history for a device.
    """
    return await it_client.get_maintenance_history(
        device_id=device_id,
        )


# ==========================================================
# Register Device Tools
# ==========================================================

tool_registry.register("create_device", create_device)
tool_registry.register("list_devices", list_devices)
tool_registry.register("get_device", get_device)
tool_registry.register("update_device", update_device)
tool_registry.register("delete_device", delete_device)
tool_registry.register("assign_device", assign_device)
tool_registry.register("return_device", return_device)
tool_registry.register("add_maintenance_log", add_maintenance_log)
tool_registry.register(
    "get_maintenance_history",
    get_maintenance_history,
)