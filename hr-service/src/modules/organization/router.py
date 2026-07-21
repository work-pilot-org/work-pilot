from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db

from .schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse,
    BranchCreate,
    BranchUpdate,
    BranchResponse,
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse,
)

from .service import (
    DepartmentService,
    DesignationService,
    BranchService,
    ShiftService,
)

router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)

@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=201,
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
):
    return DepartmentService.create(db, department)


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
    db: Session = Depends(get_db),
):
    return DepartmentService.update(db, department_id, department)


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
    db: Session = Depends(get_db),
):
    return DesignationService.create(db, designation)


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
    db: Session = Depends(get_db),
):
    return DesignationService.update(db, designation_id, designation)


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
    
                