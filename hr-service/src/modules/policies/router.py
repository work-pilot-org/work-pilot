from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.modules.policies.schemas import (
    LeavePolicyCreate, LeavePolicyUpdate, LeavePolicyResponse,
    AttendancePolicyCreate, AttendancePolicyUpdate, AttendancePolicyResponse,
    ShiftPolicyCreate, ShiftPolicyUpdate, ShiftPolicyResponse,
    HolidayPolicyCreate, HolidayPolicyUpdate, HolidayPolicyResponse,
    ProbationPolicyCreate, ProbationPolicyUpdate, ProbationPolicyResponse,
)
from src.modules.policies.service import (
    LeavePolicyService,
    AttendancePolicyService,
    ShiftPolicyService,
    HolidayPolicyService,
    ProbationPolicyService,
)

# ==================================================================
# Leave Policies Router
# ==================================================================
leave_policy_router = APIRouter(prefix="/leave-policies", tags=["Leave Policies"])

@leave_policy_router.post("", response_model=LeavePolicyResponse, status_code=status.HTTP_201_CREATED)
def create_leave_policy(policy: LeavePolicyCreate, db: Session = Depends(get_db)):
    return LeavePolicyService(db).create(policy)

@leave_policy_router.get("", response_model=list[LeavePolicyResponse])
def get_leave_policies(db: Session = Depends(get_db)):
    return LeavePolicyService(db).get_all()

@leave_policy_router.get("/{id}", response_model=LeavePolicyResponse)
def get_leave_policy(id: UUID, db: Session = Depends(get_db)):
    return LeavePolicyService(db).get_by_id(id)

@leave_policy_router.put("/{id}", response_model=LeavePolicyResponse)
def update_leave_policy(id: UUID, policy: LeavePolicyUpdate, db: Session = Depends(get_db)):
    return LeavePolicyService(db).update(id, policy)

@leave_policy_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_policy(id: UUID, db: Session = Depends(get_db)):
    LeavePolicyService(db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Attendance Policies Router
# ==================================================================
attendance_policy_router = APIRouter(prefix="/attendance-policies", tags=["Attendance Policies"])

@attendance_policy_router.post("", response_model=AttendancePolicyResponse, status_code=status.HTTP_201_CREATED)
def create_attendance_policy(policy: AttendancePolicyCreate, db: Session = Depends(get_db)):
    return AttendancePolicyService(db).create(policy)

@attendance_policy_router.get("", response_model=list[AttendancePolicyResponse])
def get_attendance_policies(db: Session = Depends(get_db)):
    return AttendancePolicyService(db).get_all()

@attendance_policy_router.get("/{id}", response_model=AttendancePolicyResponse)
def get_attendance_policy(id: UUID, db: Session = Depends(get_db)):
    return AttendancePolicyService(db).get_by_id(id)

@attendance_policy_router.put("/{id}", response_model=AttendancePolicyResponse)
def update_attendance_policy(id: UUID, policy: AttendancePolicyUpdate, db: Session = Depends(get_db)):
    return AttendancePolicyService(db).update(id, policy)

@attendance_policy_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_policy(id: UUID, db: Session = Depends(get_db)):
    AttendancePolicyService(db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Shift Policies Router
# ==================================================================
shift_policy_router = APIRouter(prefix="/shift-policies", tags=["Shift Policies"])

@shift_policy_router.post("", response_model=ShiftPolicyResponse, status_code=status.HTTP_201_CREATED)
def create_shift_policy(policy: ShiftPolicyCreate, db: Session = Depends(get_db)):
    return ShiftPolicyService(db).create(policy)

@shift_policy_router.get("", response_model=list[ShiftPolicyResponse])
def get_shift_policies(db: Session = Depends(get_db)):
    return ShiftPolicyService(db).get_all()

@shift_policy_router.get("/{id}", response_model=ShiftPolicyResponse)
def get_shift_policy(id: UUID, db: Session = Depends(get_db)):
    return ShiftPolicyService(db).get_by_id(id)

@shift_policy_router.put("/{id}", response_model=ShiftPolicyResponse)
def update_shift_policy(id: UUID, policy: ShiftPolicyUpdate, db: Session = Depends(get_db)):
    return ShiftPolicyService(db).update(id, policy)

@shift_policy_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_policy(id: UUID, db: Session = Depends(get_db)):
    ShiftPolicyService(db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Holiday Policies Router
# ==================================================================
holiday_policy_router = APIRouter(prefix="/holiday-policies", tags=["Holiday Policies"])

@holiday_policy_router.post("", response_model=HolidayPolicyResponse, status_code=status.HTTP_201_CREATED)
def create_holiday_policy(policy: HolidayPolicyCreate, db: Session = Depends(get_db)):
    return HolidayPolicyService(db).create(policy)

@holiday_policy_router.get("", response_model=list[HolidayPolicyResponse])
def get_holiday_policies(db: Session = Depends(get_db)):
    return HolidayPolicyService(db).get_all()

@holiday_policy_router.get("/{id}", response_model=HolidayPolicyResponse)
def get_holiday_policy(id: UUID, db: Session = Depends(get_db)):
    return HolidayPolicyService(db).get_by_id(id)

@holiday_policy_router.put("/{id}", response_model=HolidayPolicyResponse)
def update_holiday_policy(id: UUID, policy: HolidayPolicyUpdate, db: Session = Depends(get_db)):
    return HolidayPolicyService(db).update(id, policy)

@holiday_policy_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holiday_policy(id: UUID, db: Session = Depends(get_db)):
    HolidayPolicyService(db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ==================================================================
# Probation Policies Router
# ==================================================================
probation_policy_router = APIRouter(prefix="/probation-policies", tags=["Probation Policies"])

@probation_policy_router.post("", response_model=ProbationPolicyResponse, status_code=status.HTTP_201_CREATED)
def create_probation_policy(policy: ProbationPolicyCreate, db: Session = Depends(get_db)):
    return ProbationPolicyService(db).create(policy)

@probation_policy_router.get("", response_model=list[ProbationPolicyResponse])
def get_probation_policies(db: Session = Depends(get_db)):
    return ProbationPolicyService(db).get_all()

@probation_policy_router.get("/{id}", response_model=ProbationPolicyResponse)
def get_probation_policy(id: UUID, db: Session = Depends(get_db)):
    return ProbationPolicyService(db).get_by_id(id)

@probation_policy_router.put("/{id}", response_model=ProbationPolicyResponse)
def update_probation_policy(id: UUID, policy: ProbationPolicyUpdate, db: Session = Depends(get_db)):
    return ProbationPolicyService(db).update(id, policy)

@probation_policy_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_probation_policy(id: UUID, db: Session = Depends(get_db)):
    ProbationPolicyService(db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Temporary fix to support backward compatibility for `from src.modules.policies.router import router`
router = leave_policy_router
