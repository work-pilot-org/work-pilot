from typing import Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from src.modules.employee.models import (
    Employee,
    EmployeeDocument,
    EmployeeProfile,
)


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Employee
    # =====================================================

    def create_employee(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)
        return employee

    def get_employee_by_id(
        self,
        employee_id: UUID,
    ) -> Optional[Employee]:
        result = self.db.execute(
            select(Employee)
            .where(
                Employee.id == employee_id,
                Employee.is_active.is_(True),
            )
            .options(
                selectinload(Employee.profile),
                selectinload(Employee.documents),
            )
        )
        return result.scalar_one_or_none()

    def get_employee_by_auth_user_id(
        self,
        auth_user_id: UUID,
    ) -> Optional[Employee]:
        result = self.db.execute(
            select(Employee).where(
                Employee.auth_user_id == auth_user_id,
                Employee.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    def get_employee_by_code(
        self,
        employee_code: str,
    ) -> Optional[Employee]:
        result = self.db.execute(
            select(Employee).where(
                Employee.employee_code == employee_code,
                Employee.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    def get_all_employees(self) -> list[Employee]:
        result = self.db.execute(
            select(Employee)
            .where(Employee.is_active.is_(True))
            .options(
                selectinload(Employee.profile),
                selectinload(Employee.documents),
            )
            .order_by(Employee.created_at.desc())
        )
        return result.scalars().all()

    def update_employee(
        self,
        employee: Employee,
    ) -> Employee:
        self.db.flush()
        self.db.refresh(employee)
        return employee

    def delete_employee(
        self,
        employee: Employee,
    ) -> Employee:
        employee.is_active = False
        self.db.flush()
        self.db.refresh(employee)
        return employee

    def search_employees(
        self,
        keyword: str,
        page: int = 1,
        size: int = 10,
    ) -> list[Employee]:
        query = (
            select(Employee)
            .where(
                Employee.is_active.is_(True),
                or_(
                    Employee.first_name.ilike(f"%{keyword}%"),
                    Employee.last_name.ilike(f"%{keyword}%"),
                    Employee.employee_code.ilike(f"%{keyword}%"),
                ),
            )
            .options(
                selectinload(Employee.profile),
                selectinload(Employee.documents),
            )
            .order_by(Employee.created_at.desc())
        )
        result = self.db.execute(
            query.offset((page - 1) * size).limit(size)
        )
        return result.scalars().all()

    # =====================================================
    # Employee Profile
    # =====================================================

    def create_profile(
        self,
        profile: EmployeeProfile,
    ) -> EmployeeProfile:
        self.db.add(profile)
        self.db.flush()
        self.db.refresh(profile)
        return profile

    def get_profile(
        self,
        employee_id: UUID,
    ) -> Optional[EmployeeProfile]:
        result = self.db.execute(
            select(EmployeeProfile).where(
                EmployeeProfile.employee_id == employee_id
            )
        )
        return result.scalar_one_or_none()

    def update_profile(
        self,
        profile: EmployeeProfile,
    ) -> EmployeeProfile:
        self.db.flush()
        self.db.refresh(profile)
        return profile

    # =====================================================
    # Employee Documents
    # =====================================================

    def upload_document(
        self,
        document: EmployeeDocument,
    ) -> EmployeeDocument:
        self.db.add(document)
        self.db.flush()
        self.db.refresh(document)
        return document

    def get_documents(
        self,
        employee_id: UUID,
    ) -> list[EmployeeDocument]:
        result = self.db.execute(
            select(EmployeeDocument)
            .where(
                EmployeeDocument.employee_id == employee_id
            )
            .order_by(EmployeeDocument.uploaded_at.desc())
        )
        return result.scalars().all()

    def get_document_by_id(
        self,
        document_id: UUID,
    ) -> Optional[EmployeeDocument]:
        result = self.db.execute(
            select(EmployeeDocument).where(
                EmployeeDocument.id == document_id
            )
        )
        return result.scalar_one_or_none()

    def delete_document(
        self,
        document: EmployeeDocument,
    ) -> None:
        self.db.delete(document)
        self.db.flush()
