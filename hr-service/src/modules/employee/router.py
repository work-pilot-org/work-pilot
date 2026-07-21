from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db

from src.modules.employee.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeProfileUpdate,
    EmployeeProfileResponse,
    EmployeeDocumentCreate,
    EmployeeDocumentResponse,
)

from src.modules.employee.service import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


# =====================================================
# Employee
# =====================================================

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=201,
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.create_employee(employee)


@router.get(
    "",
    response_model=list[EmployeeResponse],
)
def get_all_employees(
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.get_all_employees()


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee_by_id(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.get_employee_by_id(employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee(
    employee_id: UUID,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.update_employee(
        employee_id,
        employee,
    )


@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def delete_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.delete_employee(employee_id)


@router.get(
    "/search/",
    response_model=list[EmployeeResponse],
)
def search_employees(
    keyword: str = Query(..., min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.search_employees(keyword, page=page, size=size)


# =====================================================
# Employee Profile
# =====================================================

@router.get(
    "/{employee_id}/profile",
    response_model=EmployeeProfileResponse,
)
def get_employee_profile(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.get_employee_profile(employee_id)


@router.put(
    "/{employee_id}/profile",
    response_model=EmployeeProfileResponse,
)
def update_employee_profile(
    employee_id: UUID,
    profile: EmployeeProfileUpdate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.update_employee_profile(
        employee_id,
        profile,
    )


# =====================================================
# Employee Documents
# =====================================================

@router.post(
    "/{employee_id}/documents",
    response_model=EmployeeDocumentResponse,
    status_code=201,
)
def upload_document(
    employee_id: UUID,
    document: EmployeeDocumentCreate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.upload_document(
        employee_id,
        document,
    )


@router.get(
    "/{employee_id}/documents",
    response_model=list[EmployeeDocumentResponse],
)
def get_documents(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return service.get_documents(employee_id)


@router.delete(
    "/{employee_id}/documents/{document_id}",
)
def delete_document(
    employee_id: UUID,
    document_id: UUID,
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    service.delete_document(
        employee_id,
        document_id,
    )

    return {
        "message": "Document deleted successfully."
    }
