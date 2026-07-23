from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.modules.employee.exceptions import (
    EmployeeAlreadyExistsException,
    EmployeeCodeAlreadyExistsException,
    EmployeeDocumentNotFoundException,
    EmployeeNotFoundException,
    EmployeeProfileNotFoundException,
)
from src.modules.employee.models import Employee, EmployeeDocument, EmployeeProfile
from src.modules.employee.repository import EmployeeRepository
from src.modules.employee.schemas import (
    EmployeeCreate,
    EmployeeDocumentCreate,
    EmployeeProfileUpdate,
    EmployeeUpdate,
)


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    # =====================================================
    # Create Employee
    # =====================================================

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        existing_employee = self.repository.get_employee_by_auth_user_id(
            employee_data.auth_user_id
        )
        if existing_employee:
            raise EmployeeAlreadyExistsException()

        existing_code = self.repository.get_employee_by_code(
            employee_data.employee_code
        )
        if existing_code:
            raise EmployeeCodeAlreadyExistsException()

        employee = Employee(
            auth_user_id=employee_data.auth_user_id,
            employee_code=employee_data.employee_code,
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            phone=employee_data.phone,
            gender=employee_data.gender.value if employee_data.gender else None,
            date_of_birth=employee_data.date_of_birth,
            joining_date=employee_data.joining_date,
            employment_type=(
                employee_data.employment_type.value
                if employee_data.employment_type
                else None
            ),
            employment_status=(
                employee_data.employment_status.value
                if employee_data.employment_status
                else None
            ),
            department_id=employee_data.department_id,
            designation_id=employee_data.designation_id,
            manager_id=employee_data.manager_id,
            work_location=employee_data.work_location,
            profile_photo=employee_data.profile_photo,
        )

        try:
            employee = self.repository.create_employee(employee)
            self.db.commit()
            return employee
        except IntegrityError:
            self.db.rollback()
            raise EmployeeAlreadyExistsException()

    # =====================================================
    # Get Employee By Id
    # =====================================================

    def get_employee_by_id(self, employee_id: UUID) -> Employee:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()
        return employee

    # =====================================================
    # Get All Employees
    # =====================================================

    def get_all_employees(self) -> list[Employee]:
        return self.repository.get_all_employees()

    # =====================================================
    # Update Employee
    # =====================================================

    def update_employee(
        self,
        employee_id: UUID,
        employee_data: EmployeeUpdate,
    ) -> Employee:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        if (
            employee_data.employee_code
            and employee_data.employee_code != employee.employee_code
        ):
            existing_employee = self.repository.get_employee_by_code(
                employee_data.employee_code
            )
            if existing_employee:
                raise EmployeeCodeAlreadyExistsException()

        update_data = employee_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(value, "value"):
                value = value.value
            setattr(employee, field, value)

        employee = self.repository.update_employee(employee)
        self.db.commit()
        return employee

    # =====================================================
    # Delete Employee (Soft Delete)
    # =====================================================

    def delete_employee(self, employee_id: UUID) -> Employee:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        employee = self.repository.delete_employee(employee)
        self.db.commit()
        return employee

    # =====================================================
    # Search Employees
    # =====================================================

    def search_employees(
        self,
        keyword: str,
        page: int = 1,
        size: int = 10,
    ) -> list[Employee]:
        keyword = keyword.strip()
        if not keyword:
            return []
        return self.repository.search_employees(keyword, page=page, size=size)

    # =====================================================
    # Get Employee Profile
    # =====================================================

    def get_employee_profile(self, employee_id: UUID) -> EmployeeProfile:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        profile = self.repository.get_profile(employee_id)
        if not profile:
            raise EmployeeProfileNotFoundException()

        return profile

    # =====================================================
    # Update Employee Profile
    # =====================================================

    def update_employee_profile(
        self,
        employee_id: UUID,
        profile_data: EmployeeProfileUpdate,
    ) -> EmployeeProfile:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        profile = self.repository.get_profile(employee_id)
        if not profile:
            profile = EmployeeProfile(employee_id=employee_id)
            profile = self.repository.create_profile(profile)

        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(value, "value"):
                value = value.value
            setattr(profile, field, value)

        profile = self.repository.update_profile(profile)
        self.db.commit()
        return profile

    # =====================================================
    # Upload Employee Document
    # =====================================================

    def upload_document(
        self,
        employee_id: UUID,
        document_data: EmployeeDocumentCreate,
    ) -> EmployeeDocument:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        document = EmployeeDocument(
            employee_id=employee_id,
            document_name=document_data.document_name,
            document_type=document_data.document_type.value,
            file_url=document_data.file_url,
        )

        document = self.repository.upload_document(document)
        self.db.commit()
        return document

    # =====================================================
    # Get Employee Documents
    # =====================================================

    def get_documents(self, employee_id: UUID) -> list[EmployeeDocument]:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        return self.repository.get_documents(employee_id)

    # =====================================================
    # Delete Employee Document
    # =====================================================

    def delete_document(self, employee_id: UUID, document_id: UUID) -> None:
        employee = self.repository.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException()

        document = self.repository.get_document_by_id(document_id)
        if not document:
            raise EmployeeDocumentNotFoundException()

        if document.employee_id != employee_id:
            raise EmployeeDocumentNotFoundException()

        self.repository.delete_document(document)
        self.db.commit()
