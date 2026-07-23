from sqlalchemy.orm import Session
from sqlalchemy import func

from src.modules.leave.models import LeaveTypeConfig, LeaveRequest, LeaveBalance, LeaveStatus, LeaveType, Holiday
from src.modules.employee.models import Employee
from src.modules.leave.schemas import (
    LeaveTypeCreate,
    LeaveTypeUpdate,
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveBalanceCreate,
    LeaveBalanceUpdate,
    HolidayCreate,
)
from uuid import UUID
from decimal import Decimal
from datetime import date


# ==================================================================
# LeaveTypeRepository
# ==================================================================

class LeaveTypeRepository:
    """Repository for Leave Type Config operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, leave_type: LeaveTypeCreate) -> LeaveTypeConfig:
        """Create a new leave type config."""

        db_leave_type = LeaveTypeConfig(**leave_type.model_dump())

        self.db.add(db_leave_type)
        self.db.flush()
        self.db.refresh(db_leave_type)

        return db_leave_type

    def get_all(self) -> list[LeaveTypeConfig]:
        """Retrieve all active leave types."""

        return (
            self.db.query(LeaveTypeConfig)
            .filter(LeaveTypeConfig.is_active == True)
            .order_by(LeaveTypeConfig.name)
            .all()
        )

    def get_by_id(self, leave_type_id: int) -> LeaveTypeConfig | None:
        """Retrieve a leave type by ID."""

        return (
            self.db.query(LeaveTypeConfig)
            .filter(
                LeaveTypeConfig.id == leave_type_id,
                LeaveTypeConfig.is_active == True,
            )
            .first()
        )

    def get_by_name(self, name: str) -> LeaveTypeConfig | None:
        """Retrieve a leave type by name."""

        return (
            self.db.query(LeaveTypeConfig)
            .filter(
                LeaveTypeConfig.name == name,
                LeaveTypeConfig.is_active == True,
            )
            .first()
        )

    def update(
        self,
        db_leave_type: LeaveTypeConfig,
        leave_type: LeaveTypeUpdate,
    ) -> LeaveTypeConfig:
        """Update an existing leave type."""

        update_data = leave_type.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_leave_type, key, value)

        self.db.flush()
        self.db.refresh(db_leave_type)

        return db_leave_type

    def delete(self, db_leave_type: LeaveTypeConfig) -> LeaveTypeConfig:
        """Soft delete a leave type."""

        db_leave_type.is_active = False

        self.db.flush()
        self.db.refresh(db_leave_type)

        return db_leave_type


# ==================================================================
# LeaveRequestRepository
# ==================================================================

class LeaveRequestRepository:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------
    # Create
    # --------------------------------------------------------

    def create(
        self,
        leave_request: LeaveRequest,
    ) -> LeaveRequest:

        self.db.add(leave_request)
        self.db.flush()
        self.db.refresh(leave_request)

        return leave_request

    # --------------------------------------------------------
    # Get By ID
    # --------------------------------------------------------

    def get_by_id(
        self,
        leave_request_id: UUID,
    ) -> LeaveRequest | None:

        return (
            self.db.query(LeaveRequest)
            .filter(
                LeaveRequest.id == leave_request_id
            )
            .first()
        )

    # --------------------------------------------------------
    # Get All
    # --------------------------------------------------------

    def get_all(self) -> list[LeaveRequest]:

        return (
            self.db.query(LeaveRequest)
            .order_by(
                LeaveRequest.created_at.desc()
            )
            .all()
        )

    # --------------------------------------------------------
    # Get Employee Leave Requests
    # --------------------------------------------------------

    def get_by_employee(
        self,
        employee_id: UUID,
    ) -> list[LeaveRequest]:

        return (
            self.db.query(LeaveRequest)
            .filter(
                LeaveRequest.employee_id == employee_id
            )
            .order_by(
                LeaveRequest.created_at.desc()
            )
            .all()
        )

    # --------------------------------------------------------
    # Get Employee Requests by Status
    # --------------------------------------------------------

    def get_by_employee_and_status(
        self,
        employee_id: UUID,
        status: LeaveStatus,
    ) -> list[LeaveRequest]:
        """Filter an employee's leave requests by a given status."""

        return (
            self.db.query(LeaveRequest)
            .filter(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status == status,
            )
            .order_by(
                LeaveRequest.created_at.desc()
            )
            .all()
        )

    # --------------------------------------------------------
    # Reporting Queries
    # --------------------------------------------------------

    def get_requests_in_range(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
        department_id: UUID | None = None,
        status: LeaveStatus | None = None,
    ) -> list[LeaveRequest]:
        """Retrieve leave requests optionally filtered by date range, department, and status."""
        query = self.db.query(LeaveRequest)

        if department_id:
            query = query.join(Employee, LeaveRequest.employee_id == Employee.id)
            query = query.filter(Employee.department_id == department_id)

        if start_date:
            query = query.filter(LeaveRequest.start_date >= start_date)

        if end_date:
            query = query.filter(LeaveRequest.end_date <= end_date)

        if status:
            query = query.filter(LeaveRequest.status == status)

        return query.order_by(LeaveRequest.start_date).all()

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(
        self,
        leave_request: LeaveRequest,
        leave_data: LeaveRequestUpdate,
    ) -> LeaveRequest:

        update_data = leave_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                leave_request,
                field,
                value,
            )

        self.db.flush()
        self.db.refresh(leave_request)

        return leave_request

    # --------------------------------------------------------
    # Cancel Leave Request
    # --------------------------------------------------------

    def cancel(
        self,
        leave_request: LeaveRequest,
    ) -> LeaveRequest:

        leave_request.status = LeaveStatus.CANCELLED

        self.db.flush()
        self.db.refresh(leave_request)

        return leave_request

    # --------------------------------------------------------
    # Update Status
    # (Called by Workflow Consumer)
    # --------------------------------------------------------

    def update_status(
        self,
        leave_request: LeaveRequest,
        status: LeaveStatus,
    ) -> LeaveRequest:

        if status == LeaveStatus.APPROVED and leave_request.status != LeaveStatus.APPROVED:
            balance = (
                self.db.query(LeaveBalance)
                .filter(
                    LeaveBalance.employee_id == leave_request.employee_id,
                    LeaveBalance.leave_type == leave_request.leave_type,
                    LeaveBalance.year == leave_request.start_date.year,
                )
                .first()
            )
            if balance:
                balance.used_days += Decimal(str(leave_request.total_days))
                
        elif leave_request.status == LeaveStatus.APPROVED and status != LeaveStatus.APPROVED:
            balance = (
                self.db.query(LeaveBalance)
                .filter(
                    LeaveBalance.employee_id == leave_request.employee_id,
                    LeaveBalance.leave_type == leave_request.leave_type,
                    LeaveBalance.year == leave_request.start_date.year,
                )
                .first()
            )
            if balance:
                balance.used_days -= Decimal(str(leave_request.total_days))

        leave_request.status = status

        self.db.flush()
        self.db.refresh(leave_request)

        return leave_request

    # --------------------------------------------------------
    # Update Workflow Instance
    # --------------------------------------------------------

    def update_workflow_instance(
        self,
        leave_request: LeaveRequest,
        workflow_instance_id: UUID,
    ) -> LeaveRequest:

        leave_request.workflow_instance_id = workflow_instance_id

        self.db.flush()
        self.db.refresh(leave_request)

        return leave_request

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    def delete(
        self,
        leave_request: LeaveRequest,
    ) -> None:

        self.db.delete(leave_request)
        self.db.flush()


# ==================================================================
# LeaveBalanceRepository
# ==================================================================

class LeaveBalanceRepository:
    """Repository for Leave Balance CRUD and employee-scoped queries."""

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------
    # Create / Allocate
    # --------------------------------------------------------

    def create(self, balance_data: LeaveBalanceCreate) -> LeaveBalance:
        """Allocate a new leave balance for an employee."""

        db_balance = LeaveBalance(
            employee_id=balance_data.employee_id,
            leave_type=balance_data.leave_type,
            year=balance_data.year,
            allocated_days=balance_data.allocated_days,
            carried_forward_days=balance_data.carried_forward_days,
            used_days=Decimal("0.0"),
            notes=balance_data.notes,
        )

        self.db.add(db_balance)
        self.db.flush()
        self.db.refresh(db_balance)

        return db_balance

    # --------------------------------------------------------
    # Get All
    # --------------------------------------------------------

    def get_all(self) -> list[LeaveBalance]:
        """Retrieve leave balances for all employees."""

        return (
            self.db.query(LeaveBalance)
            .order_by(
                LeaveBalance.employee_id,
                LeaveBalance.year.desc(),
                LeaveBalance.leave_type,
            )
            .all()
        )

    # --------------------------------------------------------
    # Get By ID
    # --------------------------------------------------------

    def get_by_id(self, balance_id: UUID) -> LeaveBalance | None:
        """Retrieve a specific leave balance record."""

        return (
            self.db.query(LeaveBalance)
            .filter(LeaveBalance.id == balance_id)
            .first()
        )

    # --------------------------------------------------------
    # Get By Employee
    # --------------------------------------------------------

    def get_by_employee(self, employee_id: UUID) -> list[LeaveBalance]:
        """Retrieve all leave balance records for an employee."""

        return (
            self.db.query(LeaveBalance)
            .filter(LeaveBalance.employee_id == employee_id)
            .order_by(
                LeaveBalance.year.desc(),
                LeaveBalance.leave_type,
            )
            .all()
        )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(
        self,
        db_balance: LeaveBalance,
        balance_data: LeaveBalanceUpdate,
    ) -> LeaveBalance:
        """Update an existing leave balance record."""

        update_data = balance_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_balance, field, value)

        self.db.flush()
        self.db.refresh(db_balance)

        return db_balance

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    def delete(self, db_balance: LeaveBalance) -> None:
        """Hard delete a leave balance record."""

        self.db.delete(db_balance)
        self.db.flush()


# ==================================================================
# HolidayRepository
# ==================================================================

class HolidayRepository:
    """Repository for Holiday operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, holiday_data: HolidayCreate) -> Holiday:
        db_holiday = Holiday(**holiday_data.model_dump())
        self.db.add(db_holiday)
        self.db.flush()
        self.db.refresh(db_holiday)
        return db_holiday

    def get_all(self) -> list[Holiday]:
        return self.db.query(Holiday).order_by(Holiday.date).all()

    def get_in_range(self, start_date: date, end_date: date) -> list[Holiday]:
        return (
            self.db.query(Holiday)
            .filter(Holiday.date >= start_date, Holiday.date <= end_date)
            .order_by(Holiday.date)
            .all()
        )

    def get_by_id(self, holiday_id: UUID) -> Holiday | None:
        return self.db.query(Holiday).filter(Holiday.id == holiday_id).first()

    def delete(self, db_holiday: Holiday) -> None:
        self.db.delete(db_holiday)
        self.db.flush()