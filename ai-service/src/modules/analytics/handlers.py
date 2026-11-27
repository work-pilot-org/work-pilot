"""
Analytics tool handlers for the Analytics Agent.
"""

from __future__ import annotations

from shared_infrastructure.core.config import settings
from modules.analytics.client import AnalyticsClient
from modules.analytics.registry import analytics_tool_registry
from modules.analytics.tools import (
    GetAttendanceSummarySchema,
    GetLeaveUtilizationSchema,
    GetHeadcountSchema,
    GetTicketSummarySchema,
    GetAssetAssignmentsSchema,
    GetWorkflowPerformanceSchema,
    GetWorkflowBottlenecksSchema,
)

# Initialize the client
analytics_client = AnalyticsClient(
    base_url=settings.ANALYTICS_SERVICE_URL or "http://localhost:8007",
)


async def get_attendance_summary(
    payload: GetAttendanceSummarySchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve the attendance summary (total worked hours, overtime, etc.)."""
    return await analytics_client.get_attendance_summary(
        headers=headers,
    )


async def get_leave_utilization(
    payload: GetLeaveUtilizationSchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve leave utilization metrics."""
    return await analytics_client.get_leave_utilization(
        period=payload.period,
        department=payload.department,
        headers=headers,
    )


async def get_headcount(
    payload: GetHeadcountSchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve employee headcount metrics."""
    return await analytics_client.get_headcount(
        department=payload.department,
        employment_type=payload.employment_type,
        headers=headers,
    )


async def get_ticket_summary(
    payload: GetTicketSummarySchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve IT ticket summary metrics."""
    return await analytics_client.get_ticket_summary(
        period=payload.period,
        category=payload.category,
        headers=headers,
    )


async def get_asset_assignments(
    payload: GetAssetAssignmentsSchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve IT asset assignment metrics."""
    return await analytics_client.get_asset_assignments(
        status=payload.status,
        category=payload.category,
        headers=headers,
    )


async def get_workflow_performance(
    payload: GetWorkflowPerformanceSchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve workflow performance metrics."""
    return await analytics_client.get_workflow_performance(
        workflow_id=payload.workflow_id,
        execution_status=payload.execution_status,
        headers=headers,
    )


async def get_workflow_bottlenecks(
    payload: GetWorkflowBottlenecksSchema,
    headers: dict[str, str] | None = None,
):
    """Retrieve workflow bottlenecks."""
    return await analytics_client.get_workflow_bottlenecks(
        workflow_id=payload.workflow_id,
        step_order=payload.step_order,
        status=payload.status,
        headers=headers,
    )


# Register tools
analytics_tool_registry.register("get_attendance_summary", get_attendance_summary)
analytics_tool_registry.register("get_leave_utilization", get_leave_utilization)
analytics_tool_registry.register("get_headcount", get_headcount)
analytics_tool_registry.register("get_ticket_summary", get_ticket_summary)
analytics_tool_registry.register("get_asset_assignments", get_asset_assignments)
analytics_tool_registry.register("get_workflow_performance", get_workflow_performance)
analytics_tool_registry.register("get_workflow_bottlenecks", get_workflow_bottlenecks)
