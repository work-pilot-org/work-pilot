"""
Tool implementations for the WorkPilot Workflow Agent.
"""

from __future__ import annotations

import httpx

from shared_infrastructure.core.config import settings
from modules.workflow.registry import workflow_tool_registry


async def _make_request(
    method: str,
    endpoint: str,
    headers: dict[str, str] | None = None,
    json: dict | None = None,
    params: dict | None = None,
) -> dict:
    """Helper for making requests to the Workflow Service."""
    url = f"{settings.WORKFLOW_SERVICE_URL}{endpoint}"
    
    # ensure headers exists and contains auth
    req_headers = {}
    if headers:
        if "authorization" in headers:
            req_headers["authorization"] = headers["authorization"]
        if "x-tenant-id" in headers:
            req_headers["x-tenant-id"] = headers["x-tenant-id"]

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=req_headers,
            json=json,
            params=params,
            timeout=10.0,
        )
        response.raise_for_status()
        
        # 204 No Content has no JSON body
        if response.status_code == 204:
            return {}
            
        return response.json()


async def create_workflow(
    name: str,
    description: str | None = None,
    is_active: bool = True,
    headers: dict[str, str] | None = None,
) -> dict:
    """Create a new workflow."""
    return await _make_request(
        "POST",
        "/workflows",
        headers=headers,
        json={"name": name, "description": description, "is_active": is_active},
    )


async def get_all_workflows(
    skip: int = 0,
    limit: int = 100,
    headers: dict[str, str] | None = None,
) -> dict:
    """Retrieve a list of all workflows."""
    return {"workflows": await _make_request("GET", "/workflows", headers=headers, params={"skip": skip, "limit": limit})}


async def get_workflow(
    workflow_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Retrieve a specific workflow by its ID."""
    return await _make_request("GET", f"/workflows/{workflow_id}", headers=headers)


async def update_workflow(
    workflow_id: str,
    name: str | None = None,
    description: str | None = None,
    is_active: bool | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    """Update an existing workflow."""
    payload = {}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    if is_active is not None:
        payload["is_active"] = is_active
        
    return await _make_request(
        "PUT",
        f"/workflows/{workflow_id}",
        headers=headers,
        json=payload,
    )


async def delete_workflow(
    workflow_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Delete a workflow."""
    return await _make_request("DELETE", f"/workflows/{workflow_id}", headers=headers)


async def start_workflow_execution(
    workflow_id: str,
    entity_type: str,
    entity_id: str,
    started_by: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Start a new workflow execution."""
    return await _make_request(
        "POST",
        "/workflow-executions",
        headers=headers,
        json={
            "workflow_id": workflow_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "started_by": started_by,
        },
    )


async def get_workflow_executions(
    skip: int = 0,
    limit: int = 100,
    headers: dict[str, str] | None = None,
) -> dict:
    """Retrieve a list of all workflow executions."""
    return {"executions": await _make_request("GET", "/workflow-executions", headers=headers, params={"skip": skip, "limit": limit})}


async def get_workflow_execution(
    execution_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Retrieve a specific workflow execution by its ID."""
    return await _make_request("GET", f"/workflow-executions/{execution_id}", headers=headers)


async def approve_task(
    task_id: str,
    decision: str,
    comments: str | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    """Approve or reject a task within a workflow execution. Decision should be 'APPROVED' or 'REJECTED'."""
    return await _make_request(
        "PATCH",
        f"/tasks/{task_id}/approve",
        headers=headers,
        json={"decision": decision, "comments": comments},
    )


async def cancel_workflow(
    execution_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Cancel an ongoing workflow execution."""
    return await _make_request("PATCH", f"/workflow-executions/{execution_id}/cancel", headers=headers)


async def restart_workflow(
    execution_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Restart a cancelled or failed workflow execution."""
    return await _make_request("PATCH", f"/workflow-executions/{execution_id}/restart", headers=headers)


async def get_workflow_history(
    execution_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Retrieve the approval history of a workflow execution."""
    return {"history": await _make_request("GET", f"/workflow-executions/{execution_id}/history", headers=headers)}

workflow_tool_registry.register("create_workflow", create_workflow)
workflow_tool_registry.register("get_all_workflows", get_all_workflows)
workflow_tool_registry.register("get_workflow", get_workflow)
workflow_tool_registry.register("update_workflow", update_workflow)
workflow_tool_registry.register("delete_workflow", delete_workflow)
workflow_tool_registry.register("start_workflow_execution", start_workflow_execution)
workflow_tool_registry.register("get_workflow_executions", get_workflow_executions)
workflow_tool_registry.register("get_workflow_execution", get_workflow_execution)
workflow_tool_registry.register("approve_task", approve_task)
workflow_tool_registry.register("cancel_workflow", cancel_workflow)
workflow_tool_registry.register("restart_workflow", restart_workflow)
workflow_tool_registry.register("get_workflow_history", get_workflow_history)
