"""
Access tools for the IT Agent.
"""

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    AccessRequestStatusUpdate,
    CreateAccessRequest,
    UpdateAccessRequest,
)


async def create_access_request(payload: CreateAccessRequest, headers=None):
    return await it_client.create_access_request(payload, headers)


async def list_access_requests(headers=None):
    return await it_client.list_access_requests(headers)


async def get_access_request(request_id: UUID, headers=None):
    return await it_client.get_access_request(request_id, headers)


async def update_access_request(
    request_id: UUID,
    payload: UpdateAccessRequest,
    headers=None,
):
    return await it_client.update_access_request(
        request_id,
        payload,
        headers,
    )


async def update_access_status(
    request_id: UUID,
    payload: AccessRequestStatusUpdate,
    headers=None,
):
    return await it_client.update_access_status(
        request_id,
        payload,
        headers,
    )


async def delete_access_request(
    request_id: UUID,
    headers=None,
):
    return await it_client.delete_access_request(
        request_id,
        headers,
    )


tool_registry.register(
    "create_access_request",
    create_access_request,
)
tool_registry.register(
    "list_access_requests",
    list_access_requests,
)
tool_registry.register(
    "get_access_request",
    get_access_request,
)
tool_registry.register(
    "update_access_request",
    update_access_request,
)
tool_registry.register(
    "update_access_status",
    update_access_status,
)
tool_registry.register(
    "delete_access_request",
    delete_access_request,
)