from sqlalchemy.orm import Session
from uuid import UUID

from src.core.exceptions import ResourceNotFoundException
from src.modules.policies.schemas import (
    LeavePolicyCreate, LeavePolicyUpdate, LeavePolicyResponse,
    AttendancePolicyCreate, AttendancePolicyUpdate, AttendancePolicyResponse,
    ShiftPolicyCreate, ShiftPolicyUpdate, ShiftPolicyResponse,
    HolidayPolicyCreate, HolidayPolicyUpdate, HolidayPolicyResponse,
    ProbationPolicyCreate, ProbationPolicyUpdate, ProbationPolicyResponse,
)
from src.modules.policies.repository import (
    LeavePolicyRepository,
    AttendancePolicyRepository,
    ShiftPolicyRepository,
    HolidayPolicyRepository,
    ProbationPolicyRepository,
)

# ==================================================================
# Leave Policy Service
# ==================================================================
class LeavePolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = LeavePolicyRepository(db)

    def get_all(self) -> list[LeavePolicyResponse]:
        db_objs = self.repository.get_all()
        return [LeavePolicyResponse.model_validate(obj) for obj in db_objs]

    def get_by_id(self, id: UUID) -> LeavePolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Leave Policy not found")
        return LeavePolicyResponse.model_validate(db_obj)

    def create(self, obj_in: LeavePolicyCreate) -> LeavePolicyResponse:
        db_obj = self.repository.create(obj_in)
        self.db.commit()
        return LeavePolicyResponse.model_validate(db_obj)

    def update(self, id: UUID, obj_in: LeavePolicyUpdate) -> LeavePolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Leave Policy not found")
        db_obj = self.repository.update(db_obj, obj_in)
        self.db.commit()
        return LeavePolicyResponse.model_validate(db_obj)

    def delete(self, id: UUID) -> None:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Leave Policy not found")
        self.repository.delete(db_obj)
        self.db.commit()


# ==================================================================
# Attendance Policy Service
# ==================================================================
class AttendancePolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AttendancePolicyRepository(db)

    def get_all(self) -> list[AttendancePolicyResponse]:
        db_objs = self.repository.get_all()
        return [AttendancePolicyResponse.model_validate(obj) for obj in db_objs]

    def get_by_id(self, id: UUID) -> AttendancePolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Attendance Policy not found")
        return AttendancePolicyResponse.model_validate(db_obj)

    def create(self, obj_in: AttendancePolicyCreate) -> AttendancePolicyResponse:
        db_obj = self.repository.create(obj_in)
        self.db.commit()
        return AttendancePolicyResponse.model_validate(db_obj)

    def update(self, id: UUID, obj_in: AttendancePolicyUpdate) -> AttendancePolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Attendance Policy not found")
        db_obj = self.repository.update(db_obj, obj_in)
        self.db.commit()
        return AttendancePolicyResponse.model_validate(db_obj)

    def delete(self, id: UUID) -> None:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Attendance Policy not found")
        self.repository.delete(db_obj)
        self.db.commit()


# ==================================================================
# Shift Policy Service
# ==================================================================
class ShiftPolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ShiftPolicyRepository(db)

    def get_all(self) -> list[ShiftPolicyResponse]:
        db_objs = self.repository.get_all()
        return [ShiftPolicyResponse.model_validate(obj) for obj in db_objs]

    def get_by_id(self, id: UUID) -> ShiftPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Shift Policy not found")
        return ShiftPolicyResponse.model_validate(db_obj)

    def create(self, obj_in: ShiftPolicyCreate) -> ShiftPolicyResponse:
        db_obj = self.repository.create(obj_in)
        self.db.commit()
        return ShiftPolicyResponse.model_validate(db_obj)

    def update(self, id: UUID, obj_in: ShiftPolicyUpdate) -> ShiftPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Shift Policy not found")
        db_obj = self.repository.update(db_obj, obj_in)
        self.db.commit()
        return ShiftPolicyResponse.model_validate(db_obj)

    def delete(self, id: UUID) -> None:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Shift Policy not found")
        self.repository.delete(db_obj)
        self.db.commit()


# ==================================================================
# Holiday Policy Service
# ==================================================================
class HolidayPolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = HolidayPolicyRepository(db)

    def get_all(self) -> list[HolidayPolicyResponse]:
        db_objs = self.repository.get_all()
        return [HolidayPolicyResponse.model_validate(obj) for obj in db_objs]

    def get_by_id(self, id: UUID) -> HolidayPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Holiday Policy not found")
        return HolidayPolicyResponse.model_validate(db_obj)

    def create(self, obj_in: HolidayPolicyCreate) -> HolidayPolicyResponse:
        db_obj = self.repository.create(obj_in)
        self.db.commit()
        return HolidayPolicyResponse.model_validate(db_obj)

    def update(self, id: UUID, obj_in: HolidayPolicyUpdate) -> HolidayPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Holiday Policy not found")
        db_obj = self.repository.update(db_obj, obj_in)
        self.db.commit()
        return HolidayPolicyResponse.model_validate(db_obj)

    def delete(self, id: UUID) -> None:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Holiday Policy not found")
        self.repository.delete(db_obj)
        self.db.commit()


# ==================================================================
# Probation Policy Service
# ==================================================================
class ProbationPolicyService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProbationPolicyRepository(db)

    def get_all(self) -> list[ProbationPolicyResponse]:
        db_objs = self.repository.get_all()
        return [ProbationPolicyResponse.model_validate(obj) for obj in db_objs]

    def get_by_id(self, id: UUID) -> ProbationPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Probation Policy not found")
        return ProbationPolicyResponse.model_validate(db_obj)

    def create(self, obj_in: ProbationPolicyCreate) -> ProbationPolicyResponse:
        db_obj = self.repository.create(obj_in)
        self.db.commit()
        return ProbationPolicyResponse.model_validate(db_obj)

    def update(self, id: UUID, obj_in: ProbationPolicyUpdate) -> ProbationPolicyResponse:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Probation Policy not found")
        db_obj = self.repository.update(db_obj, obj_in)
        self.db.commit()
        return ProbationPolicyResponse.model_validate(db_obj)

    def delete(self, id: UUID) -> None:
        db_obj = self.repository.get_by_id(id)
        if not db_obj:
            raise ResourceNotFoundException("Probation Policy not found")
        self.repository.delete(db_obj)
        self.db.commit()
