"""
Help Desk tools for the IT Agent.
"""

from __future__ import annotations

from typing import Any

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    AssignTicketRequest,
    CreateTicketRequest,
    UpdateTicketRequest,
)


async def create_ticket(
    request: CreateTicketRequest,
    headers: dict[str, str] | None = None,
) -> Any:
    """
    Create a new help desk ticket.
    """
    return await it_client.create_ticket(
        payload=request.model_dump(),
        headers=headers,
    )


async def list_tickets(
    headers: dict[str, str] | None = None,
) -> Any:
    """
    List all help desk tickets.
    """
    return await it_client.list_tickets(headers=headers)


async def get_ticket(
    ticket_id: str,
    headers: dict[str, str] | None = None,
) -> Any:
    """
    Get a ticket by ID.
    """
    return await it_client.get_ticket(
        ticket_id=ticket_id,
        headers=headers,
    )


async def update_ticket(
    ticket_id: str,
    request: UpdateTicketRequest,
    headers: dict[str, str] | None = None,
) -> Any:
    """
    Update an existing ticket.
    """
    return await it_client.update_ticket(
        ticket_id=ticket_id,
        payload=request.model_dump(exclude_none=True),
        headers=headers,
    )


async def assign_ticket(
    ticket_id: str,
    request: AssignTicketRequest,
    headers: dict[str, str] | None = None,
) -> Any:
    """
    Assign a ticket to a technician.
    """
    return await it_client.assign_ticket(
        ticket_id=ticket_id,
        payload=request.model_dump(),
        headers=headers,
    )


# Register tools
tool_registry.register("create_ticket", create_ticket)
tool_registry.register("list_tickets", list_tickets)
tool_registry.register("get_ticket", get_ticket)
tool_registry.register("update_ticket", update_ticket)
tool_registry.register("assign_ticket", assign_ticket)