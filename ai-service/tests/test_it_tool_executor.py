from __future__ import annotations

from uuid import UUID

import pytest
from pydantic import BaseModel

from modules.it.registry import tool_registry
from modules.it.tool_executor import (
    ITToolExecutionError,
    ITToolExecutor,
)


class FakeAssignRequest(BaseModel):
    assigned_to: UUID


@pytest.fixture
def executor_tool():
    tool_name = "test_assign_device"

    async def fake_assign_device(
        device_id: UUID,
        payload: FakeAssignRequest,
        headers: dict[str, str] | None = None,
    ):
        return {
            "device_id": device_id,
            "assigned_to": payload.assigned_to,
            "headers": headers,
        }

    tool_registry.register(
        tool_name,
        fake_assign_device,
    )

    yield tool_name

    # Remove only the temporary test tool.
    tool_registry._tools.pop(tool_name, None)


@pytest.mark.asyncio
async def test_executor_converts_arguments_and_injects_headers(
    executor_tool,
):
    executor = ITToolExecutor()

    device_id = "550e8400-e29b-41d4-a716-446655440000"
    user_id = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

    headers = {
        "Authorization": "Bearer test-token",
        "X-Tenant-ID": "tenant-123",
    }

    result = await executor.execute(
        tool_name=executor_tool,
        arguments={
            "device_id": device_id,
            "payload": {
                "assigned_to": user_id,
            },
        },
        headers=headers,
    )

    assert isinstance(result["device_id"], UUID)
    assert isinstance(result["assigned_to"], UUID)

    assert str(result["device_id"]) == device_id
    assert str(result["assigned_to"]) == user_id

    assert result["headers"] == headers


@pytest.mark.asyncio
async def test_executor_rejects_unknown_tool():
    executor = ITToolExecutor()

    with pytest.raises(
        ITToolExecutionError,
        match="Unknown IT tool",
    ):
        await executor.execute(
            tool_name="tool_that_does_not_exist",
            arguments={},
        )


@pytest.mark.asyncio
async def test_executor_rejects_missing_required_argument(
    executor_tool,
):
    executor = ITToolExecutor()

    with pytest.raises(
        ITToolExecutionError,
        match="Missing required argument",
    ):
        await executor.execute(
            tool_name=executor_tool,
            arguments={
                "payload": {
                    "assigned_to":
                        "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                },
            },
        )


@pytest.mark.asyncio
async def test_executor_rejects_invalid_uuid(
    executor_tool,
):
    executor = ITToolExecutor()

    with pytest.raises(ITToolExecutionError):
        await executor.execute(
            tool_name=executor_tool,
            arguments={
                "device_id": "not-a-valid-uuid",
                "payload": {
                    "assigned_to":
                        "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                },
            },
        )