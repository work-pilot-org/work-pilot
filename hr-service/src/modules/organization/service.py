from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Department, Designation, Branch, Shift
from .schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DesignationCreate,
    DesignationUpdate,
    BranchCreate,
    BranchUpdate,
    ShiftCreate,
    ShiftUpdate,
)
from .repository import (
    DepartmentRepository,
    DesignationRepository,
    BranchRepository,
    ShiftRepository,
)

class DepartmentService:

    @staticmethod
    def create(db: Session, data: DepartmentCreate):

        if DepartmentRepository.get_by_name(db, data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists."
            )

        department = Department(**data.model_dump())

        try:
            department = DepartmentRepository.create(db, department)
            db.commit()
            db.refresh(department)
            return department

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return DepartmentRepository.get_all(db)

    @staticmethod
    def update(db: Session, department_id: int, data: DepartmentUpdate):

        department = DepartmentRepository.get_by_id(db, department_id)

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found."
            )

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = DepartmentRepository.get_by_name(db, update_data["name"])

            if existing and existing.id != department.id:
                raise HTTPException(
                    status_code=400,
                    detail="Department name already exists."
                )

        for key, value in update_data.items():
            setattr(department, key, value)

        try:
            db.commit()
            db.refresh(department)
            return department

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, department_id: int):

        department = DepartmentRepository.get_by_id(db, department_id)

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found."
            )

        try:
            DepartmentRepository.delete(db, department)
            db.commit()

        except Exception:
            db.rollback()
            raise

class DesignationService:

    @staticmethod
    def create(db: Session, data: DesignationCreate):

        if DesignationRepository.get_by_name(db, data.name):
            raise HTTPException(400, "Designation already exists.")

        designation = Designation(**data.model_dump())

        try:
            designation = DesignationRepository.create(db, designation)
            db.commit()
            db.refresh(designation)
            return designation

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return DesignationRepository.get_all(db)

    @staticmethod
    def update(db: Session, designation_id: int, data: DesignationUpdate):

        designation = DesignationRepository.get_by_id(db, designation_id)

        if not designation:
            raise HTTPException(404, "Designation not found.")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = DesignationRepository.get_by_name(db, update_data["name"])

            if existing and existing.id != designation.id:
                raise HTTPException(400, "Designation already exists.")

        for key, value in update_data.items():
            setattr(designation, key, value)

        try:
            db.commit()
            db.refresh(designation)
            return designation

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, designation_id: int):

        designation = DesignationRepository.get_by_id(db, designation_id)

        if not designation:
            raise HTTPException(404, "Designation not found.")

        try:
            DesignationRepository.delete(db, designation)
            db.commit()

        except Exception:
            db.rollback()
            raise
class BranchService:

    @staticmethod
    def create(db: Session, data: BranchCreate):

        if data.code:
            if BranchRepository.get_by_code(db, data.code):
                raise HTTPException(400, "Branch code already exists.")

        branch = Branch(**data.model_dump())

        try:
            branch = BranchRepository.create(db, branch)
            db.commit()
            db.refresh(branch)
            return branch

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return BranchRepository.get_all(db)

    @staticmethod
    def update(db: Session, branch_id: int, data: BranchUpdate):

        branch = BranchRepository.get_by_id(db, branch_id)

        if not branch:
            raise HTTPException(404, "Branch not found.")

        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data and update_data["code"]:

            existing = BranchRepository.get_by_code(db, update_data["code"])

            if existing and existing.id != branch.id:
                raise HTTPException(400, "Branch code already exists.")

        for key, value in update_data.items():
            setattr(branch, key, value)

        try:
            db.commit()
            db.refresh(branch)
            return branch

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, branch_id: int):

        branch = BranchRepository.get_by_id(db, branch_id)

        if not branch:
            raise HTTPException(404, "Branch not found.")

        try:
            BranchRepository.delete(db, branch)
            db.commit()

        except Exception:
            db.rollback()
            raise
class ShiftService:

    @staticmethod
    def create(db: Session, data: ShiftCreate):

        if ShiftRepository.get_by_name(db, data.name):
            raise HTTPException(400, "Shift already exists.")

        shift = Shift(**data.model_dump())

        try:
            shift = ShiftRepository.create(db, shift)
            db.commit()
            db.refresh(shift)
            return shift

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return ShiftRepository.get_all(db)

    @staticmethod
    def update(db: Session, shift_id: int, data: ShiftUpdate):

        shift = ShiftRepository.get_by_id(db, shift_id)

        if not shift:
            raise HTTPException(404, "Shift not found.")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:

            existing = ShiftRepository.get_by_name(db, update_data["name"])

            if existing and existing.id != shift.id:
                raise HTTPException(400, "Shift already exists.")

        for key, value in update_data.items():
            setattr(shift, key, value)

        try:
            db.commit()
            db.refresh(shift)
            return shift

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, shift_id: int):

        shift = ShiftRepository.get_by_id(db, shift_id)

        if not shift:
            raise HTTPException(404, "Shift not found.")

        try:
            ShiftRepository.delete(db, shift)
            db.commit()

        except Exception:
            db.rollback()
            raise                        