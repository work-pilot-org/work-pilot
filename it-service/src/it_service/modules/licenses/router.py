import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.licenses.repository import LicenseAssignmentRepository, LicenseRepository
from it_service.modules.licenses.schemas import (
    AssignLicenseRequest,
    CreateLicenseRequest,
    LicenseAssignmentResponse,
    LicenseResponse,
    UpdateLicenseRequest,
)
from it_service.modules.licenses.service import LicenseService

router = APIRouter(
    prefix="/licenses",
    tags=["Licenses"],
)


def get_license_service() -> LicenseService:
    return LicenseService(
        repository=LicenseRepository(),
        assignment_repository=LicenseAssignmentRepository(),
    )


@router.post("", response_model=LicenseResponse, status_code=status.HTTP_201_CREATED)
def create_license(
    payload: CreateLicenseRequest,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.create_license(db, payload)


@router.get("", response_model=list[LicenseResponse])
def list_licenses(
    software_id: uuid.UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.list_licenses(db, software_id=software_id, skip=skip, limit=limit)


@router.get("/{license_id}", response_model=LicenseResponse)
def get_license(
    license_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.get_license(db, license_id)


@router.put("/{license_id}", response_model=LicenseResponse)
def update_license(
    license_id: uuid.UUID,
    payload: UpdateLicenseRequest,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.update_license(db, license_id, payload)


@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(
    license_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    service.delete_license(db, license_id)


# Assignments
@router.post("/{license_id}/assign", response_model=LicenseAssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_license(
    license_id: uuid.UUID,
    payload: AssignLicenseRequest,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.assign_license(db, license_id, payload)


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_license(
    assignment_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    service.revoke_license(db, assignment_id)


@router.get("/assignments/user/{user_id}", response_model=list[LicenseAssignmentResponse])
def get_user_assignments(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: LicenseService = Depends(get_license_service),
):
    return service.get_user_assignments(db, user_id)