from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.attendance.schemas import (
    AttendanceCheckIn,
    AttendanceCheckOut,
    AttendanceCreate,
    AttendanceExportResponse,
    AttendanceResponse,
    AttendanceStatusUpdate,
    AttendanceSummaryResponse,
    AttendanceUpdate,
    MonthlyAttendanceReportResponse,
)
from src.modules.attendance.service import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


def get_service(db: Session = Depends(get_db)) -> AttendanceService:
    return AttendanceService(db)


# ----------------------------------------------------
# Check In
# ----------------------------------------------------

@router.post(
    "/check-in",
    response_model=AttendanceResponse,
    status_code=status.HTTP_200_OK,
)
def check_in(
    request: AttendanceCheckIn,
    service: AttendanceService = Depends(get_service),
):
    try:
        return service.check_in(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ----------------------------------------------------
# Check Out
# ----------------------------------------------------

@router.post(
    "/check-out",
    response_model=AttendanceResponse,
    status_code=status.HTTP_200_OK,
)
def check_out(
    request: AttendanceCheckOut,
    service: AttendanceService = Depends(get_service),
):
    try:
        return service.check_out(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ----------------------------------------------------
# Create Attendance
# ----------------------------------------------------

@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_attendance(
    request: AttendanceCreate,
    service: AttendanceService = Depends(get_service),
):
    return service.create_attendance(request)


# ----------------------------------------------------
# Get All Attendance
# ----------------------------------------------------

@router.get(
    "",
    response_model=list[AttendanceResponse],
)
def get_all_attendance(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    service: AttendanceService = Depends(get_service),
):
    return service.get_all_attendance(skip, limit)


# ----------------------------------------------------
# Get Attendance By ID
# ----------------------------------------------------

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance(
    attendance_id: int,
    service: AttendanceService = Depends(get_service),
):
    return service.get_attendance(attendance_id)


# ----------------------------------------------------
# Update Attendance
# ----------------------------------------------------

@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def update_attendance(
    attendance_id: int,
    request: AttendanceUpdate,
    service: AttendanceService = Depends(get_service),
):
    return service.update_attendance(attendance_id, request)


# ----------------------------------------------------
# Delete Attendance
# ----------------------------------------------------

@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_attendance(
    attendance_id: int,
    service: AttendanceService = Depends(get_service),
):
    service.delete_attendance(attendance_id)


# ----------------------------------------------------
# Employee Attendance
# ----------------------------------------------------

@router.get(
    "/employee/{employee_id}",
    response_model=list[AttendanceResponse],
)
def get_employee_attendance(
    employee_id: UUID,
    service: AttendanceService = Depends(get_service),
):
    return service.get_employee_attendance(employee_id)


# ----------------------------------------------------
# Employee Summary
# ----------------------------------------------------

@router.get(
    "/employee/{employee_id}/summary",
    response_model=AttendanceSummaryResponse,
)
def get_employee_summary(
    employee_id: UUID,
    service: AttendanceService = Depends(get_service),
):
    return service.get_employee_summary(employee_id)


# ----------------------------------------------------
# Attendance By Date
# ----------------------------------------------------

@router.get(
    "/date/{attendance_date}",
    response_model=list[AttendanceResponse],
)
def get_attendance_by_date(
    attendance_date: date,
    service: AttendanceService = Depends(get_service),
):
    return service.get_attendance_by_date(attendance_date)


# ----------------------------------------------------
# Today's Attendance
# ----------------------------------------------------

@router.get(
    "/today",
    response_model=list[AttendanceResponse],
)
def get_today_attendance(
    service: AttendanceService = Depends(get_service),
):
    return service.get_today_attendance()


# ----------------------------------------------------
# Active Attendance
# ----------------------------------------------------

@router.get(
    "/active",
    response_model=list[AttendanceResponse],
)
def get_active_attendance(
    service: AttendanceService = Depends(get_service),
):
    return service.get_active_attendance()


# ----------------------------------------------------
# Update Status
# ----------------------------------------------------

@router.patch(
    "/{attendance_id}/status",
    response_model=AttendanceResponse,
)
def update_status(
    attendance_id: int,
    request: AttendanceStatusUpdate,
    service: AttendanceService = Depends(get_service),
):
    return service.update_status(attendance_id, request)


# ----------------------------------------------------
# Monthly Report
# ----------------------------------------------------

@router.get(
    "/report/monthly",
    response_model=MonthlyAttendanceReportResponse,
)
def get_monthly_report(
    month: int,
    year: int,
    service: AttendanceService = Depends(get_service),
):
    return service.get_monthly_report(month, year)


# ----------------------------------------------------
# Export Attendance
# ----------------------------------------------------

@router.get(
    "/export",
    response_model=AttendanceExportResponse,
)
def export_attendance(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=1900, le=2100),
    service: AttendanceService = Depends(get_service),
):
    return service.export_attendance(month, year)
