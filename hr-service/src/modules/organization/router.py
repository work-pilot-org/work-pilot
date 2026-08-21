from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from shared_infrastructure.core.dependencies import require_permissions, get_current_user_and_set_schema
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.publisher import publish_event

from .schemas import (
    BranchCreate,
    BranchResponse,
    BranchUpdate,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    DesignationCreate,
    DesignationResponse,
    DesignationUpdate,
    ShiftCreate,
    ShiftResponse,
    ShiftUpdate,
)
from .service import (
    BranchService,
    DepartmentService,
    DesignationService,
    ShiftService,
)

router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
    dependencies=[Depends(require_permissions([Permission.ORGANIZATION_MANAGE]))],
)

@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=201,
)
def create_department(
    department: DepartmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    result = DepartmentService.create(db, department)
    
    event = EventEnvelope[dict](
        event_type="department.created",
        source="hr-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "entity_type": "department",
            "id": str(result.id),
            "name": result.name,
            "status": "active" if result.is_active else "inactive"
        }
    )
    background_tasks.add_task(publish_event, "hr.organization", event)
    return result


@router.get(
    "/departments",
    response_model=list[DepartmentResponse],
)
def get_departments(
    db: Session = Depends(get_db),
):
    return DepartmentService.get_all(db)


@router.put(
    "/departments/{department_id}",
    response_model=DepartmentResponse,
)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    result = DepartmentService.update(db, department_id, department)
    
    event = EventEnvelope[dict](
        event_type="department.updated",
        source="hr-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "entity_type": "department",
            "id": str(result.id),
            "name": result.name,
            "status": "active" if result.is_active else "inactive"
        }
    )
    background_tasks.add_task(publish_event, "hr.organization", event)
    return result


@router.delete(
    "/departments/{department_id}",
    status_code=204,
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
):
    DepartmentService.delete(db, department_id)

@router.post(
    "/designations",
    response_model=DesignationResponse,
    status_code=201,
)
def create_designation(
    designation: DesignationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    result = DesignationService.create(db, designation)
    
    event = EventEnvelope[dict](
        event_type="designation.created",
        source="hr-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "entity_type": "designation",
            "id": str(result.id),
            "name": result.name,
            "department_id": str(result.department_id) if result.department_id else None,
            "status": "active" if result.is_active else "inactive"
        }
    )
    background_tasks.add_task(publish_event, "hr.organization", event)
    return result


@router.get(
    "/designations",
    response_model=list[DesignationResponse],
)
def get_designations(
    db: Session = Depends(get_db),
):
    return DesignationService.get_all(db)


@router.put(
    "/designations/{designation_id}",
    response_model=DesignationResponse,
)
def update_designation(
    designation_id: int,
    designation: DesignationUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    result = DesignationService.update(db, designation_id, designation)
    
    event = EventEnvelope[dict](
        event_type="designation.updated",
        source="hr-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "entity_type": "designation",
            "id": str(result.id),
            "name": result.name,
            "department_id": str(result.department_id) if result.department_id else None,
            "status": "active" if result.is_active else "inactive"
        }
    )
    background_tasks.add_task(publish_event, "hr.organization", event)
    return result


@router.delete(
    "/designations/{designation_id}",
    status_code=204,
)
def delete_designation(
    designation_id: int,
    db: Session = Depends(get_db),
):
    DesignationService.delete(db, designation_id)

@router.post(
    "/branches",
    response_model=BranchResponse,
    status_code=201,
)
def create_branch(
    branch: BranchCreate,
    db: Session = Depends(get_db),
):
    return BranchService.create(db, branch)


@router.get(
    "/branches",
    response_model=list[BranchResponse],
)
def get_branches(
    db: Session = Depends(get_db),
):
    return BranchService.get_all(db)


@router.put(
    "/branches/{branch_id}",
    response_model=BranchResponse,
)
def update_branch(
    branch_id: int,
    branch: BranchUpdate,
    db: Session = Depends(get_db),
):
    return BranchService.update(db, branch_id, branch)


@router.delete(
    "/branches/{branch_id}",
    status_code=204,
)
def delete_branch(
    branch_id: int,
    db: Session = Depends(get_db),
):
    BranchService.delete(db, branch_id)

@router.post(
    "/shifts",
    response_model=ShiftResponse,
    status_code=201,
)
def create_shift(
    shift: ShiftCreate,
    db: Session = Depends(get_db),
):
    return ShiftService.create(db, shift)


@router.get(
    "/shifts",
    response_model=list[ShiftResponse],
)
def get_shifts(
    db: Session = Depends(get_db),
):
    return ShiftService.get_all(db)


@router.put(
    "/shifts/{shift_id}",
    response_model=ShiftResponse,
)
def update_shift(
    shift_id: int,
    shift: ShiftUpdate,
    db: Session = Depends(get_db),
):
    return ShiftService.update(db, shift_id, shift)


@router.delete(
    "/shifts/{shift_id}",
    status_code=204,
)
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
):
    ShiftService.delete(db, shift_id)
    
                