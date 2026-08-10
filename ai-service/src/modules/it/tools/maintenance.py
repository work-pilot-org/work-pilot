"""
Maintenance tools for the IT Agent.
"""

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    CompleteMaintenanceRequest,
    CreateMaintenanceRecord,
    UpdateMaintenanceRecord,
)


async def create_maintenance_record(payload: CreateMaintenanceRecord, headers=None):
    return await it_client.create_maintenance_record(payload, headers, headers=headers)


async def list_maintenance_records(headers=None):
    return await it_client.list_maintenance_records(headers, headers=headers)


async def get_maintenance_record(maintenance_id: UUID, headers=None):
    return await it_client.get_maintenance_record(maintenance_id, headers, headers=headers)


async def update_maintenance_record(
    maintenance_id: UUID,
    payload: UpdateMaintenanceRecord,
    headers=None,
):
    return await it_client.update_maintenance_record(
        maintenance_id,
        payload,
        headers,
    )


async def delete_maintenance_record(
    maintenance_id: UUID,
    headers=None,
):
    return await it_client.delete_maintenance_record(
        maintenance_id,
        headers,
    )


async def complete_maintenance(
    maintenance_id: UUID,
    payload: CompleteMaintenanceRequest,
    headers=None,
):
    return await it_client.complete_maintenance(
        maintenance_id,
        payload,
        headers,
    )


async def list_device_maintenance(
    device_id: UUID,
    headers=None,
):
    return await it_client.list_device_maintenance(
        device_id,
        headers,
    )


tool_registry.register(
    "create_maintenance_record",
    create_maintenance_record,
)
tool_registry.register(
    "list_maintenance_records",
    list_maintenance_records,
)
tool_registry.register(
    "get_maintenance_record",
    get_maintenance_record,
)
tool_registry.register(
    "update_maintenance_record",
    update_maintenance_record,
)
tool_registry.register(
    "delete_maintenance_record",
    delete_maintenance_record,
)
tool_registry.register(
    "complete_maintenance",
    complete_maintenance,
)
tool_registry.register(
    "list_device_maintenance",
    list_device_maintenance,
)