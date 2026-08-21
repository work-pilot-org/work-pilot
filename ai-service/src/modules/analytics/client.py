"""
Analytics Service client.

This client is responsible for communicating with the Analytics Service.
"""

from __future__ import annotations

from typing import Any

import httpx


class AnalyticsClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Any:

        request_headers = self.headers.copy()
        if "headers" in kwargs:
            extra_headers = kwargs.pop("headers")
            if extra_headers:
                request_headers.update(extra_headers)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                headers=request_headers,
                **kwargs,
            )
            response.raise_for_status()

            if response.content:
                return response.json()
            return None

    # =====================================================
    # Analytics Endpoints
    # =====================================================

    async def get_attendance_summary(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/analytics/hr/attendance-summary",
            headers=headers
        )

    async def get_leave_utilization(
        self,
        period: str | None = None,
        department: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if period: params["period"] = period
        if department: params["department"] = department
        
        return await self._request(
            "GET",
            "/analytics/hr/leave-utilization",
            params=params,
            headers=headers
        )

    async def get_headcount(
        self,
        department: str | None = None,
        employment_type: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if department: params["department"] = department
        if employment_type: params["employment_type"] = employment_type
        
        return await self._request(
            "GET",
            "/analytics/hr/headcount",
            params=params,
            headers=headers
        )

    async def get_ticket_summary(
        self,
        period: str | None = None,
        category: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if period: params["period"] = period
        if category: params["category"] = category
        
        return await self._request(
            "GET",
            "/analytics/it/ticket-summary",
            params=params,
            headers=headers
        )

    async def get_asset_assignments(
        self,
        status: str | None = None,
        category: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if status: params["status"] = status
        if category: params["category"] = category
        
        return await self._request(
            "GET",
            "/analytics/it/asset-assignments",
            params=params,
            headers=headers
        )

    async def get_workflow_performance(
        self,
        workflow_id: str | None = None,
        execution_status: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if workflow_id: params["workflow_id"] = workflow_id
        if execution_status: params["execution_status"] = execution_status
        
        return await self._request(
            "GET",
            "/analytics/workflows/performance",
            params=params,
            headers=headers
        )

    async def get_workflow_bottlenecks(
        self,
        workflow_id: str | None = None,
        step_order: int | None = None,
        status: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if workflow_id: params["workflow_id"] = workflow_id
        if step_order: params["step_order"] = step_order
        if status: params["status"] = status
        
        return await self._request(
            "GET",
            "/analytics/workflows/bottlenecks",
            params=params,
            headers=headers
        )
