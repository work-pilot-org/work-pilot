from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, time
from decimal import Decimal


# ==================================================================
# Base Policy Schemas
# ==================================================================

class PolicyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = None
    is_active: bool = True

class PolicyResponseMixin(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==================================================================
# Leave Policy Schemas
# ==================================================================

class LeavePolicyBase(PolicyBase):
    casual_leave_days: Decimal = Field(default=Decimal("0.0"))
    sick_leave_days: Decimal = Field(default=Decimal("0.0"))
    earned_leave_days: Decimal = Field(default=Decimal("0.0"))
    maternity_leave_days: Decimal = Field(default=Decimal("0.0"))
    paternity_leave_days: Decimal = Field(default=Decimal("0.0"))
    carry_forward_enabled: bool = False
    max_carry_forward: Decimal = Field(default=Decimal("0.0"))
    half_day_allowed: bool = True
    minimum_notice_days: int = 0
    requires_attachment: bool = False

class LeavePolicyCreate(LeavePolicyBase):
    pass

class LeavePolicyUpdate(LeavePolicyBase):
    name: Optional[str] = Field(None, min_length=3, max_length=150)

class LeavePolicyResponse(LeavePolicyBase, PolicyResponseMixin):
    pass


# ==================================================================
# Attendance Policy Schemas
# ==================================================================

class AttendancePolicyBase(PolicyBase):
    working_hours: Decimal = Field(default=Decimal("8.0"))
    grace_period: int = 15
    late_mark_limit: int = 3
    half_day_after_hours: Decimal = Field(default=Decimal("4.0"))
    auto_checkout: bool = False
    weekend_policy: Optional[str] = None

class AttendancePolicyCreate(AttendancePolicyBase):
    pass

class AttendancePolicyUpdate(AttendancePolicyBase):
    name: Optional[str] = Field(None, min_length=3, max_length=150)

class AttendancePolicyResponse(AttendancePolicyBase, PolicyResponseMixin):
    pass


# ==================================================================
# Shift Policy Schemas
# ==================================================================

class ShiftPolicyBase(PolicyBase):
    shift_start: time
    shift_end: time
    break_duration: int = 60
    weekly_off: Optional[str] = None
    night_shift: bool = False

class ShiftPolicyCreate(ShiftPolicyBase):
    pass

class ShiftPolicyUpdate(ShiftPolicyBase):
    name: Optional[str] = Field(None, min_length=3, max_length=150)
    shift_start: Optional[time] = None
    shift_end: Optional[time] = None

class ShiftPolicyResponse(ShiftPolicyBase, PolicyResponseMixin):
    pass


# ==================================================================
# Holiday Policy Schemas
# ==================================================================

class HolidayPolicyBase(PolicyBase):
    calendar_name: str = Field(..., max_length=150)
    country: str = Field(..., max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    floating_holidays: int = 0

class HolidayPolicyCreate(HolidayPolicyBase):
    pass

class HolidayPolicyUpdate(HolidayPolicyBase):
    name: Optional[str] = Field(None, min_length=3, max_length=150)
    calendar_name: Optional[str] = Field(None, max_length=150)
    country: Optional[str] = Field(None, max_length=100)

class HolidayPolicyResponse(HolidayPolicyBase, PolicyResponseMixin):
    pass


# ==================================================================
# Probation Policy Schemas
# ==================================================================

class ProbationPolicyBase(PolicyBase):
    duration_months: int = 6
    review_after_months: int = 3
    confirmation_required: bool = True
    notice_period: int = 30

class ProbationPolicyCreate(ProbationPolicyBase):
    pass

class ProbationPolicyUpdate(ProbationPolicyBase):
    name: Optional[str] = Field(None, min_length=3, max_length=150)

class ProbationPolicyResponse(ProbationPolicyBase, PolicyResponseMixin):
    pass
