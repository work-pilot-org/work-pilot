from sqlalchemy.orm import Session
from uuid import UUID

from src.modules.policies.models import (
    LeavePolicy,
    AttendancePolicy,
    ShiftPolicy,
    HolidayPolicy,
    ProbationPolicy,
)
from src.modules.policies.schemas import (
    LeavePolicyCreate, LeavePolicyUpdate,
    AttendancePolicyCreate, AttendancePolicyUpdate,
    ShiftPolicyCreate, ShiftPolicyUpdate,
    HolidayPolicyCreate, HolidayPolicyUpdate,
    ProbationPolicyCreate, ProbationPolicyUpdate,
)

# ==================================================================
# Leave Policy Repository
# ==================================================================
class LeavePolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[LeavePolicy]:
        return self.db.query(LeavePolicy).order_by(LeavePolicy.created_at.desc()).all()

    def get_by_id(self, id: UUID) -> LeavePolicy | None:
        return self.db.query(LeavePolicy).filter(LeavePolicy.id == id).first()

    def create(self, obj_in: LeavePolicyCreate) -> LeavePolicy:
        db_obj = LeavePolicy(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: LeavePolicy, obj_in: LeavePolicyUpdate) -> LeavePolicy:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: LeavePolicy) -> None:
        self.db.delete(db_obj)
        self.db.flush()


# ==================================================================
# Attendance Policy Repository
# ==================================================================
class AttendancePolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AttendancePolicy]:
        return self.db.query(AttendancePolicy).order_by(AttendancePolicy.created_at.desc()).all()

    def get_by_id(self, id: UUID) -> AttendancePolicy | None:
        return self.db.query(AttendancePolicy).filter(AttendancePolicy.id == id).first()

    def create(self, obj_in: AttendancePolicyCreate) -> AttendancePolicy:
        db_obj = AttendancePolicy(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: AttendancePolicy, obj_in: AttendancePolicyUpdate) -> AttendancePolicy:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: AttendancePolicy) -> None:
        self.db.delete(db_obj)
        self.db.flush()


# ==================================================================
# Shift Policy Repository
# ==================================================================
class ShiftPolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ShiftPolicy]:
        return self.db.query(ShiftPolicy).order_by(ShiftPolicy.created_at.desc()).all()

    def get_by_id(self, id: UUID) -> ShiftPolicy | None:
        return self.db.query(ShiftPolicy).filter(ShiftPolicy.id == id).first()

    def create(self, obj_in: ShiftPolicyCreate) -> ShiftPolicy:
        db_obj = ShiftPolicy(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ShiftPolicy, obj_in: ShiftPolicyUpdate) -> ShiftPolicy:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ShiftPolicy) -> None:
        self.db.delete(db_obj)
        self.db.flush()


# ==================================================================
# Holiday Policy Repository
# ==================================================================
class HolidayPolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[HolidayPolicy]:
        return self.db.query(HolidayPolicy).order_by(HolidayPolicy.created_at.desc()).all()

    def get_by_id(self, id: UUID) -> HolidayPolicy | None:
        return self.db.query(HolidayPolicy).filter(HolidayPolicy.id == id).first()

    def create(self, obj_in: HolidayPolicyCreate) -> HolidayPolicy:
        db_obj = HolidayPolicy(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: HolidayPolicy, obj_in: HolidayPolicyUpdate) -> HolidayPolicy:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: HolidayPolicy) -> None:
        self.db.delete(db_obj)
        self.db.flush()


# ==================================================================
# Probation Policy Repository
# ==================================================================
class ProbationPolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ProbationPolicy]:
        return self.db.query(ProbationPolicy).order_by(ProbationPolicy.created_at.desc()).all()

    def get_by_id(self, id: UUID) -> ProbationPolicy | None:
        return self.db.query(ProbationPolicy).filter(ProbationPolicy.id == id).first()

    def create(self, obj_in: ProbationPolicyCreate) -> ProbationPolicy:
        db_obj = ProbationPolicy(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ProbationPolicy, obj_in: ProbationPolicyUpdate) -> ProbationPolicy:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ProbationPolicy) -> None:
        self.db.delete(db_obj)
        self.db.flush()
