import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.licenses.models import License, LicenseAssignment
from it_service.modules.licenses.repository import LicenseAssignmentRepository, LicenseRepository
from it_service.modules.licenses.schemas import (
    AssignLicenseRequest,
    CreateLicenseRequest,
    UpdateLicenseRequest,
)


class LicenseService:
    def __init__(
        self,
        repository: LicenseRepository,
        assignment_repository: LicenseAssignmentRepository,
    ):
        self.repository = repository
        self.assignment_repository = assignment_repository

    def _get_license(self, db: Session, license_id: uuid.UUID) -> License:
        license = self.repository.get_by_id(db, license_id)
        if not license:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License not found.",
            )
        return license

    def create_license(self, db: Session, payload: CreateLicenseRequest) -> License:
        license = License(
            software_id=payload.software_id,
            license_key=payload.license_key,
            total_seats=payload.total_seats,
            expiry_date=payload.expiry_date,
            renewal_date=payload.renewal_date,
            used_seats=0,
        )
        return self.repository.create(db, license)

    def get_license(self, db: Session, license_id: uuid.UUID) -> License:
        return self._get_license(db, license_id)

    def list_licenses(self, db: Session, **filters) -> list[License]:
        return self.repository.list(db, **filters)

    def update_license(
        self, db: Session, license_id: uuid.UUID, payload: UpdateLicenseRequest
    ) -> License:
        license = self._get_license(db, license_id)
        updates = payload.model_dump(exclude_unset=True)
        
        if "total_seats" in updates:
            if updates["total_seats"] < license.used_seats:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot reduce total seats below currently used seats ({license.used_seats}).",
                )

        for field, value in updates.items():
            setattr(license, field, value)
            
        return self.repository.save(db, license)

    def assign_license(
        self, db: Session, license_id: uuid.UUID, payload: AssignLicenseRequest
    ) -> LicenseAssignment:
        license = self._get_license(db, license_id)
        
        # Check if already assigned to this user
        existing = self.assignment_repository.get_by_license_and_user(
            db, license_id, payload.assigned_to
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="License is already assigned to this user.",
            )

        if license.used_seats >= license.total_seats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No available seats left on this license.",
            )

        assignment = LicenseAssignment(
            license_id=license_id,
            assigned_to=payload.assigned_to,
        )
        created_assignment = self.assignment_repository.create(db, assignment)

        # Update seat count
        license.used_seats += 1
        self.repository.save(db, license)

        return created_assignment

    def revoke_license(self, db: Session, assignment_id: uuid.UUID) -> None:
        assignment = self.assignment_repository.get_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License assignment not found.",
            )
        
        license = self._get_license(db, assignment.license_id)
        
        self.assignment_repository.delete(db, assignment)
        
        # Update seat count
        if license.used_seats > 0:
            license.used_seats -= 1
            self.repository.save(db, license)

    def get_user_assignments(self, db: Session, user_id: uuid.UUID) -> list[LicenseAssignment]:
        return self.assignment_repository.list_by_user(db, user_id)

    def delete_license(self, db: Session, license_id: uuid.UUID) -> None:
        license = self._get_license(db, license_id)
        self.repository.delete(db, license)