from sqlalchemy.orm import Session
from decimal import Decimal

from src.modules.leave.models import LeaveTypeConfig, LeaveRequest, LeaveBalance, LeaveStatus, Holiday
from src.modules.leave.repository import (
    LeaveTypeRepository,
    LeaveRequestRepository,
    LeaveBalanceRepository,
    HolidayRepository,
)
from src.modules.leave.schemas import (
    LeaveTypeCreate,
    LeaveTypeUpdate,
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestListResponse,
    LeaveRequestUpdate,
    LeaveBalanceCreate,
    LeaveBalanceUpdate,
    LeaveBalanceResponse,
    LeaveBalanceSummaryItem,
    EmployeeLeaveBalanceResponse,
    LeaveSummaryItem,
    EmployeeLeaveSummaryResponse,
    HolidayCreate,
    HolidayResponse,
    LeaveReportItem,
    OrganizationLeaveReportResponse,
    MonthlyLeaveReportItem,
    MonthlyLeaveReportResponse,
    DepartmentLeaveReportResponse,
    EventType,
    CalendarEvent,
)
from src.modules.leave.exceptions import (
    LeaveTypeAlreadyExistsException,
    LeaveTypeNotFoundException,
    ResourceNotFoundException,
    BadRequestException,
    LeaveBalanceNotFoundException,
)

from uuid import UUID
from datetime import date
from src.infrastructure.clients.workflow_client import workflow_client


# ==================================================================
# Helpers
# ==================================================================

def _compute_remaining(balance: LeaveBalance) -> Decimal:
    """Calculate remaining days from a balance record."""
    return (
        Decimal(str(balance.allocated_days))
        + Decimal(str(balance.carried_forward_days))
        - Decimal(str(balance.used_days))
    )


def _balance_to_response(balance: LeaveBalance) -> LeaveBalanceResponse:
    """Serialize a LeaveBalance ORM object to its response schema."""
    return LeaveBalanceResponse(
        id=balance.id,
        employee_id=balance.employee_id,
        leave_type=balance.leave_type,
        year=balance.year,
        allocated_days=Decimal(str(balance.allocated_days)),
        used_days=Decimal(str(balance.used_days)),
        carried_forward_days=Decimal(str(balance.carried_forward_days)),
        remaining_days=_compute_remaining(balance),
        notes=balance.notes,
        created_at=balance.created_at,
        updated_at=balance.updated_at,
    )


# ==================================================================
# LeaveTypeService
# ==================================================================

class LeaveTypeService:
    """Service layer for Leave Type Config operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = LeaveTypeRepository(db)

    def create_leave_type(
        self,
        leave_type: LeaveTypeCreate,
    ) -> LeaveTypeConfig:
        """Create a new leave type."""

        existing_leave = self.repository.get_by_name(
            leave_type.name
        )

        if existing_leave:
            raise LeaveTypeAlreadyExistsException(
                "Leave type name already exists."
            )

        db_leave = self.repository.create(leave_type)

        self.db.commit()

        return db_leave

    def get_all_leave_types(self) -> list[LeaveTypeConfig]:
        """Retrieve all active leave types."""

        return self.repository.get_all()

    def get_leave_type(
        self,
        leave_type_id: int,
    ) -> LeaveTypeConfig:
        """Retrieve a leave type by ID."""

        db_leave = self.repository.get_by_id(
            leave_type_id
        )

        if not db_leave:
            raise LeaveTypeNotFoundException()

        return db_leave

    def update_leave_type(
        self,
        leave_type_id: int,
        leave_type: LeaveTypeUpdate,
    ) -> LeaveTypeConfig:
        """Update an existing leave type."""

        db_leave = self.repository.get_by_id(
            leave_type_id
        )

        if not db_leave:
            raise LeaveTypeNotFoundException()

        if (
            leave_type.name is not None
            and leave_type.name != db_leave.name
        ):
            existing_leave = self.repository.get_by_name(
                leave_type.name
            )

            if existing_leave:
                raise LeaveTypeAlreadyExistsException(
                    "Leave type name already exists."
                )

        updated_leave = self.repository.update(
            db_leave,
            leave_type,
        )

        self.db.commit()

        return updated_leave

    def delete_leave_type(
        self,
        leave_type_id: int,
    ) -> None:
        """Deactivate a leave type."""

        db_leave = self.repository.get_by_id(
            leave_type_id
        )

        if not db_leave:
            raise LeaveTypeNotFoundException()

        self.repository.delete(db_leave)
        self.db.commit()


# ==================================================================
# LeaveRequestService
# ==================================================================

class LeaveRequestService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = LeaveRequestRepository(db)
        self.workflow_client = workflow_client

    # ---------------------------------------------------------
    # Create Leave Request
    # ---------------------------------------------------------

    def create_leave_request(
        self,
        leave_data: LeaveRequestCreate,
    ) -> LeaveRequestResponse:

        try:

            if leave_data.end_date < leave_data.start_date:
                raise BadRequestException(
                    message="End date cannot be earlier than start date."
                )

            total_days = self._calculate_leave_days(
                leave_data.start_date,
                leave_data.end_date,
                leave_data.is_half_day,
            )

            leave_request = LeaveRequest(
                employee_id=leave_data.employee_id,
                leave_type=leave_data.leave_type,
                start_date=leave_data.start_date,
                end_date=leave_data.end_date,
                total_days=total_days,
                reason=leave_data.reason,
                is_half_day=leave_data.is_half_day,
                attachment_url=leave_data.attachment_url,
                emergency_contact=leave_data.emergency_contact,
                status=LeaveStatus.PENDING,
            )

            leave_request = self.repository.create(
                leave_request
            )

            self.db.commit()
            
            # Start workflow
            self.workflow_client.start_workflow(
                entity_id=leave_request.id,
                entity_type="leave_request",
                workflow_name="leave_approval",
                requested_by=leave_data.employee_id
            )

            return LeaveRequestResponse.model_validate(
                leave_request
            )

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # Get All Leave Requests
    # ---------------------------------------------------------

    def get_all_leave_requests(
        self,
    ) -> list[LeaveRequestResponse]:

        leave_requests = self.repository.get_all()

        return [
            LeaveRequestResponse.model_validate(
                leave_request
            )
            for leave_request in leave_requests
        ]

    # ---------------------------------------------------------
    # Get Leave Request By ID
    # ---------------------------------------------------------

    def get_leave_request_by_id(
        self,
        leave_request_id: UUID,
    ) -> LeaveRequestResponse:

        leave_request = self.repository.get_by_id(
            leave_request_id
        )

        if not leave_request:
            raise ResourceNotFoundException(
                message="Leave request not found."
            )

        return LeaveRequestResponse.model_validate(
            leave_request
        )

    # ---------------------------------------------------------
    # Update Leave Request
    # ---------------------------------------------------------

    def update_leave_request(
        self,
        leave_request_id: UUID,
        leave_data: LeaveRequestUpdate,
    ) -> LeaveRequestResponse:

        try:

            leave_request = self.repository.get_by_id(
                leave_request_id
            )

            if not leave_request:
                raise ResourceNotFoundException(
                    message="Leave request not found."
                )

            self._validate_pending_status(
                leave_request
            )

            total_days = self._calculate_total_days(
                leave_request,
                leave_data,
            )

            leave_request.total_days = total_days

            leave_request = self.repository.update(
                leave_request,
                leave_data,
            )

            self.db.commit()

            return LeaveRequestResponse.model_validate(
                leave_request
            )

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # Update Leave Request Status
    # ---------------------------------------------------------
    def update_leave_request_status(
        self,
        leave_request_id: UUID,
        status: LeaveStatus,
    ) -> LeaveRequestResponse:
        try:
            leave_request = self.repository.get_by_id(leave_request_id)
            if not leave_request:
                raise ResourceNotFoundException(message="Leave request not found.")
            
            leave_request.status = status
            self.db.commit()
            return LeaveRequestResponse.model_validate(leave_request)
        except Exception:
            self.db.rollback()
            raise
    # ---------------------------------------------------------
    # Cancel Leave Request
    # ---------------------------------------------------------

    def cancel_leave_request(
        self,
        leave_request_id: UUID,
    ) -> None:

        try:

            leave_request = self.repository.get_by_id(
                leave_request_id
            )

            if not leave_request:
                raise ResourceNotFoundException(
                    message="Leave request not found."
                )

            self._validate_pending_status(
                leave_request
            )

            self.repository.cancel(
                leave_request
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # GET /employees/{employee_id}/leave-requests
    # ---------------------------------------------------------

    def get_employee_leave_requests(
        self,
        employee_id: UUID,
    ) -> list[LeaveRequestListResponse]:
        """Retrieve all leave requests for a specific employee."""

        requests = self.repository.get_by_employee(employee_id)

        return [
            LeaveRequestListResponse.model_validate(r)
            for r in requests
        ]

    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    def _validate_pending_status(
        self,
        leave_request: LeaveRequest,
    ) -> None:

        if leave_request.status != LeaveStatus.PENDING:
            raise BadRequestException(
                message=(
                    "Only pending leave requests can be "
                    "updated or cancelled."
                )
            )

    def _calculate_total_days(
        self,
        leave_request: LeaveRequest,
        leave_data: LeaveRequestUpdate,
    ) -> int:

        start_date = (
            leave_data.start_date
            if leave_data.start_date is not None
            else leave_request.start_date
        )

        end_date = (
            leave_data.end_date
            if leave_data.end_date is not None
            else leave_request.end_date
        )

        is_half_day = (
            leave_data.is_half_day
            if leave_data.is_half_day is not None
            else leave_request.is_half_day
        )

        return self._calculate_leave_days(
            start_date,
            end_date,
            is_half_day,
        )

    def _calculate_leave_days(
        self,
        start_date: date,
        end_date: date,
        is_half_day: bool,
    ) -> int:

        if end_date < start_date:
            raise BadRequestException(
                message="End date cannot be earlier than start date."
            )

        if is_half_day:
            return 1

        return (end_date - start_date).days + 1


# ==================================================================
# LeaveBalanceService
# ==================================================================

class LeaveBalanceService:
    """Service layer for Leave Balance operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = LeaveBalanceRepository(db)
        self.request_repository = LeaveRequestRepository(db)

    # ---------------------------------------------------------
    # POST /leave-balances  — Allocate
    # ---------------------------------------------------------

    def allocate_leave_balance(
        self,
        balance_data: LeaveBalanceCreate,
    ) -> LeaveBalanceResponse:
        """Allocate leave balance to an employee."""

        try:
            db_balance = self.repository.create(balance_data)
            self.db.commit()
            return _balance_to_response(db_balance)

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # GET /leave-balances
    # ---------------------------------------------------------

    def get_all_leave_balances(self) -> list[LeaveBalanceResponse]:
        """Retrieve leave balances for all employees."""

        balances = self.repository.get_all()
        return [_balance_to_response(b) for b in balances]

    # ---------------------------------------------------------
    # GET /leave-balances/{balance_id}
    # ---------------------------------------------------------

    def get_leave_balance(
        self,
        balance_id: UUID,
    ) -> LeaveBalanceResponse:
        """Retrieve a specific leave balance record."""

        db_balance = self.repository.get_by_id(balance_id)

        if not db_balance:
            raise LeaveBalanceNotFoundException()

        return _balance_to_response(db_balance)

    # ---------------------------------------------------------
    # PUT /leave-balances/{balance_id}
    # ---------------------------------------------------------

    def update_leave_balance(
        self,
        balance_id: UUID,
        balance_data: LeaveBalanceUpdate,
    ) -> LeaveBalanceResponse:
        """Update an employee's leave balance."""

        try:
            db_balance = self.repository.get_by_id(balance_id)

            if not db_balance:
                raise LeaveBalanceNotFoundException()

            db_balance = self.repository.update(db_balance, balance_data)
            self.db.commit()

            return _balance_to_response(db_balance)

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # DELETE /leave-balances/{balance_id}
    # ---------------------------------------------------------

    def delete_leave_balance(self, balance_id: UUID) -> None:
        """Remove a leave balance record."""

        try:
            db_balance = self.repository.get_by_id(balance_id)

            if not db_balance:
                raise LeaveBalanceNotFoundException()

            self.repository.delete(db_balance)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # GET /employees/{employee_id}/leave-balance
    # ---------------------------------------------------------

    def get_employee_leave_balance(
        self,
        employee_id: UUID,
    ) -> EmployeeLeaveBalanceResponse:
        """Retrieve an employee's current leave balance across all types."""

        balances = self.repository.get_by_employee(employee_id)

        items = [
            LeaveBalanceSummaryItem(
                leave_type=b.leave_type,
                year=b.year,
                allocated_days=Decimal(str(b.allocated_days)),
                used_days=Decimal(str(b.used_days)),
                carried_forward_days=Decimal(str(b.carried_forward_days)),
                remaining_days=_compute_remaining(b),
            )
            for b in balances
        ]

        return EmployeeLeaveBalanceResponse(
            employee_id=employee_id,
            balances=items,
        )

    # ---------------------------------------------------------
    # GET /employees/{employee_id}/leave-summary
    # ---------------------------------------------------------

    def get_employee_leave_summary(
        self,
        employee_id: UUID,
    ) -> EmployeeLeaveSummaryResponse:
        """
        Retrieve a summary of leave usage and remaining balance
        for an employee, grouped by leave type and year.
        """

        balances = self.repository.get_by_employee(employee_id)
        all_requests = self.request_repository.get_by_employee(employee_id)

        # Index requests by (leave_type, year)
        from collections import defaultdict

        request_map: dict[tuple, list[LeaveRequest]] = defaultdict(list)
        for req in all_requests:
            key = (req.leave_type, req.start_date.year)
            request_map[key].append(req)

        summary_items: list[LeaveSummaryItem] = []

        for balance in balances:
            key = (balance.leave_type, balance.year)
            reqs = request_map.get(key, [])

            total_requested = sum(r.total_days for r in reqs)
            approved = sum(
                r.total_days for r in reqs
                if r.status == LeaveStatus.APPROVED
            )
            pending = sum(
                r.total_days for r in reqs
                if r.status == LeaveStatus.PENDING
            )
            rejected = sum(
                r.total_days for r in reqs
                if r.status == LeaveStatus.REJECTED
            )

            summary_items.append(
                LeaveSummaryItem(
                    leave_type=balance.leave_type,
                    year=balance.year,
                    total_requested_days=total_requested,
                    approved_days=approved,
                    pending_days=pending,
                    rejected_days=rejected,
                    allocated_days=Decimal(str(balance.allocated_days)),
                    used_days=Decimal(str(balance.used_days)),
                    remaining_days=_compute_remaining(balance),
                )
            )

        return EmployeeLeaveSummaryResponse(
            employee_id=employee_id,
            summary=summary_items,
        )


# ==================================================================
# HolidayService
# ==================================================================

class HolidayService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = HolidayRepository(db)

    def create_holiday(self, holiday: HolidayCreate) -> HolidayResponse:
        db_holiday = self.repository.create(holiday)
        self.db.commit()
        return HolidayResponse.model_validate(db_holiday)

    def get_all_holidays(self) -> list[HolidayResponse]:
        holidays = self.repository.get_all()
        return [HolidayResponse.model_validate(h) for h in holidays]

    def get_holiday(self, holiday_id: UUID) -> HolidayResponse:
        holiday = self.repository.get_by_id(holiday_id)
        if not holiday:
            raise ResourceNotFoundException("Holiday not found")
        return HolidayResponse.model_validate(holiday)

    def delete_holiday(self, holiday_id: UUID) -> None:
        holiday = self.repository.get_by_id(holiday_id)
        if not holiday:
            raise ResourceNotFoundException("Holiday not found")
        self.repository.delete(holiday)
        self.db.commit()


# ==================================================================
# LeaveReportService
# ==================================================================

class LeaveReportService:
    def __init__(self, db: Session):
        self.db = db
        self.request_repo = LeaveRequestRepository(db)
        self.holiday_repo = HolidayRepository(db)

    def _aggregate_reports(self, requests: list[LeaveRequest]) -> list[LeaveReportItem]:
        from collections import defaultdict
        
        stats = defaultdict(lambda: {"requested": 0, "approved": 0, "pending": 0, "rejected": 0})
        
        for req in requests:
            lt = req.leave_type
            stats[lt]["requested"] += req.total_days
            if req.status == LeaveStatus.APPROVED:
                stats[lt]["approved"] += req.total_days
            elif req.status == LeaveStatus.PENDING:
                stats[lt]["pending"] += req.total_days
            elif req.status == LeaveStatus.REJECTED:
                stats[lt]["rejected"] += req.total_days
                
        return [
            LeaveReportItem(
                leave_type=lt,
                total_requested=s["requested"],
                total_approved=s["approved"],
                total_pending=s["pending"],
                total_rejected=s["rejected"],
            )
            for lt, s in stats.items()
        ]

    def get_organization_report(self, start_date: date | None = None, end_date: date | None = None) -> OrganizationLeaveReportResponse:
        requests = self.request_repo.get_requests_in_range(start_date=start_date, end_date=end_date)
        
        employees_on_leave = len(set(r.employee_id for r in requests if r.status == LeaveStatus.APPROVED))
        
        return OrganizationLeaveReportResponse(
            start_date=start_date,
            end_date=end_date,
            total_employees_on_leave=employees_on_leave,
            report_items=self._aggregate_reports(requests)
        )

    def get_monthly_report(self, year: int, month: int | None = None) -> MonthlyLeaveReportResponse:
        start_d = date(year, month or 1, 1)
        if month:
            # next month trick for end_date
            import calendar
            last_day = calendar.monthrange(year, month)[1]
            end_d = date(year, month, last_day)
        else:
            end_d = date(year, 12, 31)
            
        requests = self.request_repo.get_requests_in_range(start_date=start_d, end_date=end_d)
        
        # Group by month
        from collections import defaultdict
        monthly_map = defaultdict(list)
        for r in requests:
            monthly_map[r.start_date.month].append(r)
            
        reports = []
        for m, reqs in sorted(monthly_map.items()):
            reports.append(
                MonthlyLeaveReportItem(
                    year=year,
                    month=m,
                    report_items=self._aggregate_reports(reqs)
                )
            )
            
        return MonthlyLeaveReportResponse(reports=reports)

    def get_department_report(self, department_id: UUID, start_date: date | None = None, end_date: date | None = None) -> DepartmentLeaveReportResponse:
        requests = self.request_repo.get_requests_in_range(start_date=start_date, end_date=end_date, department_id=department_id)
        
        employees_on_leave = len(set(r.employee_id for r in requests if r.status == LeaveStatus.APPROVED))
        
        return DepartmentLeaveReportResponse(
            department_id=department_id,
            start_date=start_date,
            end_date=end_date,
            total_employees_on_leave=employees_on_leave,
            report_items=self._aggregate_reports(requests)
        )

    def get_leave_calendar(self, start_date: date | None = None, end_date: date | None = None) -> list[CalendarEvent]:
        events = []
        
        # 1. Add approved leaves
        requests = self.request_repo.get_requests_in_range(start_date=start_date, end_date=end_date, status=LeaveStatus.APPROVED)
        for req in requests:
            events.append(
                CalendarEvent(
                    id=req.id,
                    title=f"{req.leave_type} Leave",
                    date=req.start_date,
                    event_type=EventType.LEAVE,
                    employee_id=req.employee_id,
                    leave_status=req.status,
                )
            )
            
        # 2. Add holidays
        if start_date and end_date:
            holidays = self.holiday_repo.get_in_range(start_date, end_date)
        else:
            holidays = self.holiday_repo.get_all()
            
        for h in holidays:
            events.append(
                CalendarEvent(
                    id=h.id,
                    title=h.name,
                    date=h.date,
                    event_type=EventType.HOLIDAY,
                    is_optional_holiday=h.is_optional,
                )
            )
            
        # Sort by date
        events.sort(key=lambda x: x.date)
        return events