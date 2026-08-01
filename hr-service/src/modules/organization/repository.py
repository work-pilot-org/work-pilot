from sqlalchemy.orm import Session

from .models import Department, Designation, Branch, Shift


class DepartmentRepository:

    @staticmethod
    def create(db: Session, department: Department):
        db.add(department)
        db.flush()
        db.refresh(department)
        return department

    @staticmethod
    def get_all(db: Session):
        return db.query(Department).order_by(Department.name).all()

    @staticmethod
    def get_by_id(db: Session, department_id: int):
        return (
            db.query(Department)
            .filter(Department.id == department_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return (
            db.query(Department)
            .filter(Department.name == name)
            .first()
        )

    @staticmethod
    def delete(db: Session, department: Department):
        db.delete(department)
        db.flush()


class DesignationRepository:

    @staticmethod
    def create(db: Session, designation: Designation):
        db.add(designation)
        db.flush()
        db.refresh(designation)
        return designation

    @staticmethod
    def get_all(db: Session):
        return db.query(Designation).order_by(Designation.name).all()

    @staticmethod
    def get_by_id(db: Session, designation_id: int):
        return (
            db.query(Designation)
            .filter(Designation.id == designation_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return (
            db.query(Designation)
            .filter(Designation.name == name)
            .first()
        )

    @staticmethod
    def delete(db: Session, designation: Designation):
        db.delete(designation)
        db.flush()


class BranchRepository:

    @staticmethod
    def create(db: Session, branch: Branch):
        db.add(branch)
        db.flush()
        db.refresh(branch)
        return branch

    @staticmethod
    def get_all(db: Session):
        return db.query(Branch).order_by(Branch.name).all()

    @staticmethod
    def get_by_id(db: Session, branch_id: int):
        return (
            db.query(Branch)
            .filter(Branch.id == branch_id)
            .first()
        )

    @staticmethod
    def get_by_code(db: Session, code: str):
        return (
            db.query(Branch)
            .filter(Branch.code == code)
            .first()
        )

    @staticmethod
    def delete(db: Session, branch: Branch):
        db.delete(branch)
        db.flush()


class ShiftRepository:

    @staticmethod
    def create(db: Session, shift: Shift):
        db.add(shift)
        db.flush()
        db.refresh(shift)
        return shift

    @staticmethod
    def get_all(db: Session):
        return db.query(Shift).order_by(Shift.name).all()

    @staticmethod
    def get_by_id(db: Session, shift_id: int):
        return (
            db.query(Shift)
            .filter(Shift.id == shift_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return (
            db.query(Shift)
            .filter(Shift.name == name)
            .first()
        )

    @staticmethod
    def delete(db: Session, shift: Shift):
        db.delete(shift)
        db.flush()