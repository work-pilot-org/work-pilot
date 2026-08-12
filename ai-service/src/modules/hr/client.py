"""
HR Service client.

This client is responsible for communicating with the HR Service.
"""

from __future__ import annotations

from typing import Any

import httpx


class HRClient:
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
    # Generated API Methods
    # =====================================================

    async def check_in(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/attendance/check-in",
            json=payload,
            headers=headers
        )

    async def check_out(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/attendance/check-out",
            json=payload,
            headers=headers
        )

    async def create_attendance(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/attendance",
            json=payload,
            headers=headers
        )

    async def get_all_attendance(
        self,
        skip: int = 0,
        limit: int = 100,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance",
            params={"skip": skip, "limit": limit},
            headers=headers
        )

    async def get_attendance(
        self,
        attendance_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/attendance/{attendance_id}",
            headers=headers
        )

    async def update_attendance(
        self,
        attendance_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/attendance/{attendance_id}",
            json=payload,
            headers=headers
        )

    async def delete_attendance(
        self,
        attendance_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/attendance/{attendance_id}",
            headers=headers
        )

    async def get_employee_attendance(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/attendance/employee/{employee_id}",
            headers=headers
        )

    async def attendance_summary(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/attendance/employee/{employee_id}/summary",
            headers=headers
        )

    async def get_attendance_by_date(
        self,
        attendance_date: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/attendance/date/{attendance_date}",
            headers=headers
        )

    async def today_attendance(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance/today",
            headers=headers
        )

    async def get_active_attendance(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance/active",
            headers=headers
        )

    async def update_attendance_status(
        self,
        attendance_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PATCH",
            f"/attendance/{attendance_id}/status",
            json=payload,
            headers=headers
        )

    async def monthly_report(
        self,
        year: int,
        month: int | None = None,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance/report/monthly",
            params={"year": year, "month": month},
            headers=headers
        )

    async def export_attendance(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance/export",
            headers=headers
        )

    async def create_employee(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/employees",
            json=payload,
            headers=headers
        )

    async def get_all_employees(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/employees",
            headers=headers
        )

    async def get_employee(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}",
            headers=headers
        )

    async def update_employee(
        self,
        employee_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/employees/{employee_id}",
            json=payload,
            headers=headers
        )

    async def delete_employee(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/employees/{employee_id}",
            headers=headers
        )

    async def search_employee(
        self,
        keyword: str,
        page: int = 1,
        size: int = 10,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/employees/search/",
            params={"keyword": keyword, "page": page, "size": size},
            headers=headers
        )

    async def get_employee_profile(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}/profile",
            headers=headers
        )

    async def update_employee_profile(
        self,
        employee_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/employees/{employee_id}/profile",
            json=payload,
            headers=headers
        )

    async def upload_document(
        self,
        employee_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            f"/employees/{employee_id}/documents",
            json=payload,
            headers=headers
        )

    async def get_documents(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}/documents",
            headers=headers
        )

    async def delete_document(
        self,
        employee_id: str,
        document_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/employees/{employee_id}/documents/{document_id}",
            headers=headers
        )

    async def create_leave_type(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/leave-types",
            json=payload,
            headers=headers
        )

    async def get_leave_types(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave-types",
            headers=headers
        )

    async def get_leave_type(
        self,
        leave_type_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/leave-types/{leave_type_id}",
            headers=headers
        )

    async def update_leave_type(
        self,
        leave_type_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/leave-types/{leave_type_id}",
            json=payload,
            headers=headers
        )

    async def delete_leave_type(
        self,
        leave_type_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/leave-types/{leave_type_id}",
            headers=headers
        )

    async def create_leave_request(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/leave-requests",
            json=payload,
            headers=headers
        )

    async def get_all_leave_requests(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave-requests",
            headers=headers
        )

    async def get_leave_request(
        self,
        leave_request_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/leave-requests/{leave_request_id}",
            headers=headers
        )

    async def update_leave_request(
        self,
        leave_request_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/leave-requests/{leave_request_id}",
            json=payload,
            headers=headers
        )

    async def update_leave_request_status(
        self,
        leave_request_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PATCH",
            f"/leave-requests/{leave_request_id}/status",
            json=payload,
            headers=headers
        )

    async def cancel_leave_request(
        self,
        leave_request_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/leave-requests/{leave_request_id}",
            headers=headers
        )

    async def get_employee_leave_requests(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}/leave-requests",
            headers=headers
        )

    async def get_employee_leave_balance(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}/leave-balance",
            headers=headers
        )

    async def get_employee_leave_summary(
        self,
        employee_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/employees/{employee_id}/leave-summary",
            headers=headers
        )

    async def create_leave_balance(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/leave-balances",
            json=payload,
            headers=headers
        )

    async def bulk_create_leave_balance(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/leave-balances/bulk",
            json=payload,
            headers=headers
        )

    async def get_all_leave_balances(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave-balances",
            headers=headers
        )

    async def get_leave_balance(
        self,
        balance_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/leave-balances/{balance_id}",
            headers=headers
        )

    async def update_leave_balance(
        self,
        balance_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/leave-balances/{balance_id}",
            json=payload,
            headers=headers
        )

    async def delete_leave_balance(
        self,
        balance_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/leave-balances/{balance_id}",
            headers=headers
        )

    async def organization_leave_report(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave/reports",
            headers=headers
        )

    async def monthly_leave_report(
        self,
        year: int,
        month: int | None = None,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave/reports/monthly",
            params={
                "year": year,
                "month": month,
            },
            headers=headers
        )

    async def department_leave_report(
        self,
        department_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/leave/reports/department/{department_id}",
            headers=headers
        )

    async def leave_calendar(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._request(
            "GET",
            "/leave/calendar",
            params=params,
            headers=headers
        )

    async def create_holiday(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/holidays",
            json=payload,
            headers=headers
        )

    async def get_holidays(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/holidays",
            headers=headers
        )

    async def delete_holiday(
        self,
        holiday_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/holidays/{holiday_id}",
            headers=headers
        )

    async def create_department(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/organization/departments",
            json=payload,
            headers=headers
        )

    async def get_departments(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/organization/departments",
            headers=headers
        )

    async def update_department(
        self,
        department_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/organization/departments/{department_id}",
            json=payload,
            headers=headers
        )

    async def delete_department(
        self,
        department_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/organization/departments/{department_id}",
            headers=headers
        )

    async def create_designation(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/organization/designations",
            json=payload,
            headers=headers
        )

    async def get_designations(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/organization/designations",
            headers=headers
        )

    async def update_designation(
        self,
        designation_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/organization/designations/{designation_id}",
            json=payload,
            headers=headers
        )

    async def delete_designation(
        self,
        designation_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/organization/designations/{designation_id}",
            headers=headers
        )

    async def create_branch(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/organization/branches",
            json=payload,
            headers=headers
        )

    async def get_branches(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/organization/branches",
            headers=headers
        )

    async def update_branch(
        self,
        branch_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/organization/branches/{branch_id}",
            json=payload,
            headers=headers
        )

    async def delete_branch(
        self,
        branch_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/organization/branches/{branch_id}",
            headers=headers
        )

    async def create_shift(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/organization/shifts",
            json=payload,
            headers=headers
        )

    async def get_shifts(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/organization/shifts",
            headers=headers
        )

    async def update_shift(
        self,
        shift_id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/organization/shifts/{shift_id}",
            json=payload,
            headers=headers
        )

    async def delete_shift(
        self,
        shift_id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/organization/shifts/{shift_id}",
            headers=headers
        )

    async def create_leave_policies(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/leave-policies",
            json=payload,
            headers=headers
        )

    async def get_leave_policies(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/leave-policies",
            headers=headers
        )

    async def get_leave_policies_by_id(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/leave-policies/{id}",
            headers=headers
        )

    async def update_leave_policies(
        self,
        id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/leave-policies/{id}",
            json=payload,
            headers=headers
        )

    async def delete_leave_policies(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/leave-policies/{id}",
            headers=headers
        )

    async def create_attendance_policies(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/attendance-policies",
            json=payload,
            headers=headers
        )

    async def get_attendance_policies(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/attendance-policies",
            headers=headers
        )

    async def get_attendance_policies_by_id(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/attendance-policies/{id}",
            headers=headers
        )

    async def update_attendance_policies(
        self,
        id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/attendance-policies/{id}",
            json=payload,
            headers=headers
        )

    async def delete_attendance_policies(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/attendance-policies/{id}",
            headers=headers
        )

    async def create_shift_policies(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/shift-policies",
            json=payload,
            headers=headers
        )

    async def get_shift_policies(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/shift-policies",
            headers=headers
        )

    async def get_shift_policies_by_id(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/shift-policies/{id}",
            headers=headers
        )

    async def update_shift_policies(
        self,
        id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/shift-policies/{id}",
            json=payload,
            headers=headers
        )

    async def delete_shift_policies(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/shift-policies/{id}",
            headers=headers
        )

    async def create_holiday_policies(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/holiday-policies",
            json=payload,
            headers=headers
        )

    async def get_holiday_policies(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/holiday-policies",
            headers=headers
        )

    async def get_holiday_policies_by_id(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/holiday-policies/{id}",
            headers=headers
        )

    async def update_holiday_policies(
        self,
        id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/holiday-policies/{id}",
            json=payload,
            headers=headers
        )

    async def delete_holiday_policies(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/holiday-policies/{id}",
            headers=headers
        )

    async def create_probation_policies(
        self,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "POST",
            "/probation-policies",
            json=payload,
            headers=headers
        )

    async def get_probation_policies(
        self,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            "/probation-policies",
            headers=headers
        )

    async def get_probation_policies_by_id(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "GET",
            f"/probation-policies/{id}",
            headers=headers
        )

    async def update_probation_policies(
        self,
        id: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "PUT",
            f"/probation-policies/{id}",
            json=payload,
            headers=headers
        )

    async def delete_probation_policies(
        self,
        id: str,
        headers: dict[str, str] | None = None,
    ):
        return await self._request(
            "DELETE",
            f"/probation-policies/{id}",
            headers=headers
        )


from shared_infrastructure.core.config import settings

hr_client = HRClient(
    base_url=settings.hr_service_url,
)

