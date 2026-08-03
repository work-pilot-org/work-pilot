from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from shared_infrastructure.core.dependencies import (
    get_current_user_and_set_schema,
    require_permissions,
    verify_employee_ownership,
)
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
from src.modules.employee.schemas import (
    EmployeeCreate,
    EmployeeDocumentCreate,
    EmployeeDocumentResponse,
    EmployeeProfileResponse,
    EmployeeProfileUpdate,
    EmployeeResponse,
    EmployeeUpdate,
)
from src.modules.employee.service import EmployeeService
from shared_infrastructure.core.security import get_current_user

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(get_current_user_and_set_schema)],
)

# =====================================================
# Employee
# =====================================================

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=201,
    dependencies=[Depends(require_permissions([Permission.EMPLOYEE_MANAGE]))],
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
    dependencies=[Depends(require_permissions([Permission.EMPLOYEE_MANAGE]))],
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
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
    service = EmployeeService(db)
    return service.get_employee_by_id(employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_permissions([Permission.EMPLOYEE_MANAGE]))],
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
    dependencies=[Depends(require_permissions([Permission.EMPLOYEE_MANAGE]))],
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
    dependencies=[Depends(require_permissions([Permission.EMPLOYEE_MANAGE]))],
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
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
    service = EmployeeService(db)
    return service.get_employee_profile(employee_id)


@router.put(
    "/{employee_id}/profile",
    response_model=EmployeeProfileResponse,
)
def update_employee_profile(
    employee_id: UUID,
    profile: EmployeeProfileUpdate,
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
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
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
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
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
    service = EmployeeService(db)
    return service.get_documents(employee_id)


@router.delete(
    "/{employee_id}/documents/{document_id}",
)
def delete_document(
    employee_id: UUID,
    document_id: UUID,
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    verify_employee_ownership(employee_id, current_user, db, bypass_permissions=[Permission.EMPLOYEE_MANAGE])
    service = EmployeeService(db)
    service.delete_document(
        employee_id,
        document_id,
    )

    return {
        "message": "Document deleted successfully."
    }
