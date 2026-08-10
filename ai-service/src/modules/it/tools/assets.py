"""
Asset tools for the IT Agent.
"""

from __future__ import annotations

from uuid import UUID

from infrastructure.integrations.it_client import it_client
from modules.it.registry import tool_registry
from modules.it.schemas import (
    AssignAssetRequest,
    CreateAssetRequest,
    UpdateAssetRequest,
)

# ==========================================================
# Asset Tools
# ==========================================================

async def create_asset(
    payload: CreateAssetRequest,
    headers: dict[str, str] | None = None,
):
    """
    Create a new IT asset.
    """
    return await it_client.create_asset(
        payload=payload,
        )


async def list_assets(
    *,
    category: str | None = None,
    status: str | None = None,
    assigned_to: UUID | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    headers: dict[str, str] | None = None,
):
    """
    List IT assets.
    """
    return await it_client.list_assets(
        category=category,
        status=status,
        assigned_to=assigned_to,
        search=search,
        skip=skip,
        limit=limit,
        )


async def get_asset(
    asset_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Retrieve an asset by ID.
    """
    return await it_client.get_asset(
        asset_id=asset_id,
        )


async def update_asset(
    asset_id: UUID,
    payload: UpdateAssetRequest,
    headers: dict[str, str] | None = None,
):
    """
    Update an asset.
    """
    return await it_client.update_asset(
        asset_id=asset_id,
        payload=payload,
        )


async def delete_asset(
    asset_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Delete an asset.
    """
    return await it_client.delete_asset(
        asset_id=asset_id,
        )


async def assign_asset(
    asset_id: UUID,
    payload: AssignAssetRequest,
    headers: dict[str, str] | None = None,
):
    """
    Assign an asset to a user.
    """
    return await it_client.assign_asset(
        asset_id=asset_id,
        payload=payload,
        )


async def return_asset(
    asset_id: UUID,
    headers: dict[str, str] | None = None,
):
    """
    Return an assigned asset.
    """
    return await it_client.return_asset(
        asset_id=asset_id,
        )


# ==========================================================
# Register Tools
# ==========================================================

tool_registry.register("create_asset", create_asset)
tool_registry.register("list_assets", list_assets)
tool_registry.register("get_asset", get_asset)
tool_registry.register("update_asset", update_asset)
tool_registry.register("delete_asset", delete_asset)
tool_registry.register("assign_asset", assign_asset)
tool_registry.register("return_asset", return_asset)