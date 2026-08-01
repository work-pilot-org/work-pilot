from sqlalchemy import (
    Boolean,
    Integer,
    Numeric,
    String,
    Text,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import TenantBase

from enum import Enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


# ------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------

class LeaveType(str, Enum):
    CASUAL = "CASUAL"
    SICK = "SICK"
    EARNED = "EARNED"
    MATERNITY = "MATERNITY"
    PATERNITY = "PATERNITY"
    COMP_OFF = "COMP_OFF"
    UNPAID = "UNPAID"
    OTHER = "OTHER"


class LeaveStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


# ------------------------------------------------------------------
# LeaveTypeConfig  (configurable leave type definitions)
# ------------------------------------------------------------------

class LeaveTypeConfig(TenantBase):
    """Configurable leave type definitions (e.g. annual entitlement)."""

    __tablename__ = "leave_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    days_per_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_paid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    carry_forward: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


# ------------------------------------------------------------------
# LeaveRequest
# ------------------------------------------------------------------

class LeaveRequest(TenantBase):
    __tablename__ = "leave_requests"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    leave_type = Column(
        SqlEnum(LeaveType, name="leave_type_enum"),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    total_days = Column(
        Integer,
        nullable=False,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    is_half_day = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    attachment_url = Column(
        String(500),
        nullable=True,
    )

    emergency_contact = Column(
        String(100),
        nullable=True,
    )

    status = Column(
        SqlEnum(LeaveStatus, name="leave_status_enum"),
        default=LeaveStatus.PENDING,
        nullable=False,
    )

    workflow_instance_id = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    employee = relationship(
        "Employee",
        back_populates="leave_requests",
    )


# ------------------------------------------------------------------
# LeaveBalance
# ------------------------------------------------------------------

class LeaveBalance(TenantBase):
    """Tracks allocated, used, and remaining leave days per employee per leave type per year."""

    __tablename__ = "leave_balances"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    leave_type = Column(
        SqlEnum(LeaveType, name="leave_type_enum"),
        nullable=False,
    )

    year = Column(
        Integer,
        nullable=False,
    )

    allocated_days = Column(
        Numeric(5, 1),
        nullable=False,
        default=0,
    )

    used_days = Column(
        Numeric(5, 1),
        nullable=False,
        default=0,
    )

    carried_forward_days = Column(
        Numeric(5, 1),
        nullable=False,
        default=0,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    employee = relationship(
        "Employee",
        back_populates="leave_balances",
    )


# ------------------------------------------------------------------
# Holiday
# ------------------------------------------------------------------

class Holiday(TenantBase):
    """Tracks organization holidays for the leave calendar."""

    __tablename__ = "holidays"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    date = Column(
        Date,
        nullable=False,
        index=True,
    )

    is_optional = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )