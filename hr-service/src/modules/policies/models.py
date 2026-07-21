from sqlalchemy import Column, String, Text, Boolean, Integer, Numeric, Time, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.infrastructure.database.base import TenantBase


# ==================================================================
# Base Policy Model (Mixins can be used, but explicit models are preferred)
# ==================================================================

class PolicyMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ==================================================================
# Leave Policy
# ==================================================================

class LeavePolicy(TenantBase, PolicyMixin):
    __tablename__ = "leave_policies"

    casual_leave_days = Column(Numeric(5, 1), default=0, nullable=False)
    sick_leave_days = Column(Numeric(5, 1), default=0, nullable=False)
    earned_leave_days = Column(Numeric(5, 1), default=0, nullable=False)
    maternity_leave_days = Column(Numeric(5, 1), default=0, nullable=False)
    paternity_leave_days = Column(Numeric(5, 1), default=0, nullable=False)

    carry_forward_enabled = Column(Boolean, default=False, nullable=False)
    max_carry_forward = Column(Numeric(5, 1), default=0, nullable=False)

    half_day_allowed = Column(Boolean, default=True, nullable=False)
    minimum_notice_days = Column(Integer, default=0, nullable=False)
    requires_attachment = Column(Boolean, default=False, nullable=False)


# ==================================================================
# Attendance Policy
# ==================================================================

class AttendancePolicy(TenantBase, PolicyMixin):
    __tablename__ = "attendance_policies"

    working_hours = Column(Numeric(4, 2), default=8.0, nullable=False)
    grace_period = Column(Integer, default=15, nullable=False)  # in minutes
    late_mark_limit = Column(Integer, default=3, nullable=False) # late marks before penalty
    half_day_after_hours = Column(Numeric(4, 2), default=4.0, nullable=False)
    auto_checkout = Column(Boolean, default=False, nullable=False)
    weekend_policy = Column(String(100), nullable=True)  # e.g., 'SAT_SUN_OFF'


# ==================================================================
# Shift Policy
# ==================================================================

class ShiftPolicy(TenantBase, PolicyMixin):
    __tablename__ = "shift_policies"

    shift_start = Column(Time, nullable=False)
    shift_end = Column(Time, nullable=False)
    break_duration = Column(Integer, default=60, nullable=False)  # in minutes
    weekly_off = Column(String(50), nullable=True)  # e.g., 'Sunday'
    night_shift = Column(Boolean, default=False, nullable=False)


# ==================================================================
# Holiday Policy
# ==================================================================

class HolidayPolicy(TenantBase, PolicyMixin):
    __tablename__ = "holiday_policies"

    calendar_name = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    floating_holidays = Column(Integer, default=0, nullable=False)


# ==================================================================
# Probation Policy
# ==================================================================

class ProbationPolicy(TenantBase, PolicyMixin):
    __tablename__ = "probation_policies"

    duration_months = Column(Integer, default=6, nullable=False)
    review_after_months = Column(Integer, default=3, nullable=False)
    confirmation_required = Column(Boolean, default=True, nullable=False)
    notice_period = Column(Integer, default=30, nullable=False)  # in days
