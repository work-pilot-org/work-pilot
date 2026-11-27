from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from it_service.modules.licenses.models import License, LicenseAssignment


class LicenseRepository:
    def create(self, db: Session, license: License) -> License:
        db.add(license)
        db.commit()
        db.refresh(license)
        return license

    def get_by_id(self, db: Session, license_id: UUID) -> License | None:
        statement = select(License).where(License.id == license_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        software_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[License]:
        statement = select(License)

        if software_id:
            statement = statement.where(License.software_id == software_id)

        statement = statement.order_by(desc(License.created_at)).offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def save(self, db: Session, license: License) -> License:
        db.commit()
        db.refresh(license)
        return license

    def delete(self, db: Session, license: License) -> None:
        db.delete(license)
        db.commit()


class LicenseAssignmentRepository:
    def create(self, db: Session, assignment: LicenseAssignment) -> LicenseAssignment:
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    def get_by_id(self, db: Session, assignment_id: UUID) -> LicenseAssignment | None:
        statement = select(LicenseAssignment).where(LicenseAssignment.id == assignment_id)
        return db.scalar(statement)

    def get_by_license_and_user(
        self, db: Session, license_id: UUID, assigned_to: UUID
    ) -> LicenseAssignment | None:
        statement = select(LicenseAssignment).where(
            LicenseAssignment.license_id == license_id,
            LicenseAssignment.assigned_to == assigned_to,
        )
        return db.scalar(statement)

    def list_by_license(self, db: Session, license_id: UUID) -> list[LicenseAssignment]:
        statement = select(LicenseAssignment).where(LicenseAssignment.license_id == license_id)
        return list(db.scalars(statement).all())

    def list_by_user(self, db: Session, assigned_to: UUID) -> list[LicenseAssignment]:
        statement = select(LicenseAssignment).where(LicenseAssignment.assigned_to == assigned_to)
        return list(db.scalars(statement).all())

    def delete(self, db: Session, assignment: LicenseAssignment) -> None:
        db.delete(assignment)
        db.commit()