from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.leave.schemas import (
    LeaveTypeCreate,
    LeaveTypeResponse,
    LeaveTypeUpdate,
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestResponse,
    LeaveRequestListResponse,
    LeaveBalanceCreate,
    LeaveBalanceUpdate,
    LeaveBalanceResponse,
    EmployeeLeaveBalanceResponse,
    EmployeeLeaveSummaryResponse,
    OrganizationLeaveReportResponse,
    MonthlyLeaveReportResponse,
    DepartmentLeaveReportResponse,
    HolidayCreate,
    HolidayResponse,
    CalendarEvent,
)
from src.modules.leave.service import (
    LeaveTypeService,
    LeaveRequestService,
    LeaveBalanceService,
    LeaveReportService,
    HolidayService,
)

from uuid import UUID
from datetime import date
from typing import Optional


# ==================================================================
# Leave Types Router
# ==================================================================

leave_type_router = APIRouter(
    prefix="/leave-types",
    tags=["Leave Types"],
)


@leave_type_router.post(
    "",
    response_model=LeaveTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_type(
    leave_type: LeaveTypeCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new leave type.
    """
    service = LeaveTypeService(db)
    return service.create_leave_type(leave_type)


@leave_type_router.get(
    "",
    response_model=list[LeaveTypeResponse],
)
def get_leave_types(
    db: Session = Depends(get_db),
):
    """
    Retrieve all leave types.
    """
    service = LeaveTypeService(db)
    return service.get_all_leave_types()


@leave_type_router.get(
    "/{leave_type_id}",
    response_model=LeaveTypeResponse,
)
def get_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific leave type.
    """
    service = LeaveTypeService(db)
    return service.get_leave_type(leave_type_id)


@leave_type_router.put(
    "/{leave_type_id}",
    response_model=LeaveTypeResponse,
)
def update_leave_type(
    leave_type_id: int,
    leave_type: LeaveTypeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a leave type.
    """
    service = LeaveTypeService(db)
    return service.update_leave_type(
        leave_type_id,
        leave_type,
    )


@leave_type_router.delete(
    "/{leave_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
):
    """
    Deactivate a leave type.
    """
    service = LeaveTypeService(db)
    service.delete_leave_type(leave_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Leave Requests Router
# ==================================================================

leave_request_router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"],
)


# -------------------------------------------------------------------
# Submit Leave Request
# -------------------------------------------------------------------

@leave_request_router.post(
    "",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    leave_request: LeaveRequestCreate,
    db: Session = Depends(get_db),
):
    """Submit a new leave request."""
    service = LeaveRequestService(db)
    return service.create_leave_request(leave_request)


# -------------------------------------------------------------------
# Get All Leave Requests
# -------------------------------------------------------------------

@leave_request_router.get(
    "",
    response_model=list[LeaveRequestResponse],
)
def get_all_leave_requests(
    db: Session = Depends(get_db),
):
    """Retrieve all leave requests."""
    service = LeaveRequestService(db)
    return service.get_all_leave_requests()


# -------------------------------------------------------------------
# Get Leave Request By ID
# -------------------------------------------------------------------

@leave_request_router.get(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse,
)
def get_leave_request(
    leave_request_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve a specific leave request."""
    service = LeaveRequestService(db)
    return service.get_leave_request_by_id(leave_request_id)


# -------------------------------------------------------------------
# Update Leave Request
# -------------------------------------------------------------------

@leave_request_router.put(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse,
)
def update_leave_request(
    leave_request_id: UUID,
    leave_request: LeaveRequestUpdate,
    db: Session = Depends(get_db),
):
    """Update a pending leave request."""
    service = LeaveRequestService(db)
    return service.update_leave_request(
        leave_request_id,
        leave_request,
    )


# -------------------------------------------------------------------
# Cancel Leave Request
# -------------------------------------------------------------------

@leave_request_router.delete(
    "/{leave_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_leave_request(
    leave_request_id: UUID,
    db: Session = Depends(get_db),
):
    """Cancel a pending leave request."""
    service = LeaveRequestService(db)
    service.cancel_leave_request(leave_request_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Employee Leave Router  (/employees/{employee_id}/...)
# ==================================================================

employee_leave_router = APIRouter(
    prefix="/employees",
    tags=["Employee Leave"],
)


# -------------------------------------------------------------------
# GET /employees/{employee_id}/leave-requests
# -------------------------------------------------------------------

@employee_leave_router.get(
    "/{employee_id}/leave-requests",
    response_model=list[LeaveRequestListResponse],
    summary="Get Employee Leave Requests",
)
def get_employee_leave_requests(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve all leave requests for a specific employee."""
    service = LeaveRequestService(db)
    return service.get_employee_leave_requests(employee_id)


# -------------------------------------------------------------------
# GET /employees/{employee_id}/leave-balance
# -------------------------------------------------------------------

@employee_leave_router.get(
    "/{employee_id}/leave-balance",
    response_model=EmployeeLeaveBalanceResponse,
    summary="Get Employee Leave Balance",
)
def get_employee_leave_balance(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve the employee's current leave balance across all leave types."""
    service = LeaveBalanceService(db)
    return service.get_employee_leave_balance(employee_id)


# -------------------------------------------------------------------
# GET /employees/{employee_id}/leave-summary
# -------------------------------------------------------------------

@employee_leave_router.get(
    "/{employee_id}/leave-summary",
    response_model=EmployeeLeaveSummaryResponse,
    summary="Get Employee Leave Summary",
)
def get_employee_leave_summary(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve a summary of leave usage and remaining balance for an employee."""
    service = LeaveBalanceService(db)
    return service.get_employee_leave_summary(employee_id)


# ==================================================================
# Leave Balance Router  (/leave-balances)
# ==================================================================

leave_balance_router = APIRouter(
    prefix="/leave-balances",
    tags=["Leave Balance Management"],
)


# -------------------------------------------------------------------
# POST /leave-balances  — Allocate
# -------------------------------------------------------------------

@leave_balance_router.post(
    "",
    response_model=LeaveBalanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Allocate Leave Balance",
)
def allocate_leave_balance(
    balance: LeaveBalanceCreate,
    db: Session = Depends(get_db),
):
    """Allocate leave balance to an employee."""
    service = LeaveBalanceService(db)
    return service.allocate_leave_balance(balance)


# -------------------------------------------------------------------
# GET /leave-balances
# -------------------------------------------------------------------

@leave_balance_router.get(
    "",
    response_model=list[LeaveBalanceResponse],
    summary="Get All Leave Balances",
)
def get_all_leave_balances(
    db: Session = Depends(get_db),
):
    """Retrieve leave balances for all employees."""
    service = LeaveBalanceService(db)
    return service.get_all_leave_balances()


# -------------------------------------------------------------------
# GET /leave-balances/{balance_id}
# -------------------------------------------------------------------

@leave_balance_router.get(
    "/{balance_id}",
    response_model=LeaveBalanceResponse,
    summary="Get Leave Balance",
)
def get_leave_balance(
    balance_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve a specific leave balance record."""
    service = LeaveBalanceService(db)
    return service.get_leave_balance(balance_id)


# -------------------------------------------------------------------
# PUT /leave-balances/{balance_id}
# -------------------------------------------------------------------

@leave_balance_router.put(
    "/{balance_id}",
    response_model=LeaveBalanceResponse,
    summary="Update Leave Balance",
)
def update_leave_balance(
    balance_id: UUID,
    balance: LeaveBalanceUpdate,
    db: Session = Depends(get_db),
):
    """Update an employee's leave balance."""
    service = LeaveBalanceService(db)
    return service.update_leave_balance(balance_id, balance)


# -------------------------------------------------------------------
# DELETE /leave-balances/{balance_id}
# -------------------------------------------------------------------

@leave_balance_router.delete(
    "/{balance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Leave Balance",
)
def delete_leave_balance(
    balance_id: UUID,
    db: Session = Depends(get_db),
):
    """Remove a leave balance record."""
    service = LeaveBalanceService(db)
    service.delete_leave_balance(balance_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Backward-compat alias — main.py imports `router`
# ==================================================================

# Keep the existing import in main.py working by aliasing
# the leave_request_router as `router`.  New routers are
# imported individually in main.py.
router = leave_request_router


# ==================================================================
# Leave Reports Router (/leave/reports)
# ==================================================================

leave_report_router = APIRouter(
    prefix="/leave/reports",
    tags=["Leave Reports"],
)

@leave_report_router.get(
    "",
    response_model=OrganizationLeaveReportResponse,
    summary="Get Organization Leave Report",
)
def get_organization_leave_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """Retrieve organization-wide leave reports."""
    service = LeaveReportService(db)
    return service.get_organization_report(start_date, end_date)

@leave_report_router.get(
    "/monthly",
    response_model=MonthlyLeaveReportResponse,
    summary="Get Monthly Leave Report",
)
def get_monthly_leave_report(
    year: int,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Retrieve monthly leave reports."""
    service = LeaveReportService(db)
    return service.get_monthly_report(year, month)

@leave_report_router.get(
    "/department/{department_id}",
    response_model=DepartmentLeaveReportResponse,
    summary="Get Department Leave Report",
)
def get_department_leave_report(
    department_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """Retrieve department-wise leave reports."""
    service = LeaveReportService(db)
    return service.get_department_report(department_id, start_date, end_date)


# ==================================================================
# Leave Calendar Router (/leave/calendar)
# ==================================================================

leave_calendar_router = APIRouter(
    prefix="/leave/calendar",
    tags=["Leave Calendar"],
)

@leave_calendar_router.get(
    "",
    response_model=list[CalendarEvent],
    summary="Get Leave Calendar",
)
def get_leave_calendar(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """Retrieve the leave calendar showing approved leaves and holidays."""
    service = LeaveReportService(db)
    return service.get_leave_calendar(start_date, end_date)


# ==================================================================
# Holiday Router (/holidays)
# ==================================================================

holiday_router = APIRouter(
    prefix="/holidays",
    tags=["Holidays"],
)

@holiday_router.post(
    "",
    response_model=HolidayResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Holiday",
)
def create_holiday(
    holiday: HolidayCreate,
    db: Session = Depends(get_db),
):
    """Add a new holiday."""
    service = HolidayService(db)
    return service.create_holiday(holiday)

@holiday_router.get(
    "",
    response_model=list[HolidayResponse],
    summary="Get All Holidays",
)
def get_all_holidays(
    db: Session = Depends(get_db),
):
    """Retrieve all holidays."""
    service = HolidayService(db)
    return service.get_all_holidays()

@holiday_router.delete(
    "/{holiday_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Holiday",
)
def delete_holiday(
    holiday_id: UUID,
    db: Session = Depends(get_db),
):
    """Remove a holiday."""
    service = HolidayService(db)
    service.delete_holiday(holiday_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)