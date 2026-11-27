from uuid import UUID

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session

from it_service.modules.software.enums import InstallationRequestStatus
from it_service.modules.software.models import InstallationRequest, InstalledSoftware, Software


class SoftwareRepository:
    def create(self, db: Session, software: Software) -> Software:
        db.add(software)
        db.commit()
        db.refresh(software)
        return software

    def get_by_id(self, db: Session, software_id: UUID) -> Software | None:
        statement = select(Software).where(Software.id == software_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Software]:
        statement = select(Software)

        if search:
            statement = statement.where(
                or_(
                    Software.name.ilike(f"%{search}%"),
                    Software.publisher.ilike(f"%{search}%"),
                )
            )

        statement = statement.order_by(asc(Software.name)).offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def save(self, db: Session, software: Software) -> Software:
        db.commit()
        db.refresh(software)
        return software

    def delete(self, db: Session, software: Software) -> None:
        db.delete(software)
        db.commit()


class InstalledSoftwareRepository:
    def create(self, db: Session, install: InstalledSoftware) -> InstalledSoftware:
        db.add(install)
        db.commit()
        db.refresh(install)
        return install

    def get_by_id(self, db: Session, install_id: UUID) -> InstalledSoftware | None:
        statement = select(InstalledSoftware).where(InstalledSoftware.id == install_id)
        return db.scalar(statement)

    def get_by_software_and_device(
        self, db: Session, software_id: UUID, device_id: UUID
    ) -> InstalledSoftware | None:
        statement = select(InstalledSoftware).where(
            InstalledSoftware.software_id == software_id,
            InstalledSoftware.device_id == device_id,
        )
        return db.scalar(statement)

    def get_by_software_and_user(
        self, db: Session, software_id: UUID, user_id: UUID
    ) -> InstalledSoftware | None:
        statement = select(InstalledSoftware).where(
            InstalledSoftware.software_id == software_id,
            InstalledSoftware.user_id == user_id,
        )
        return db.scalar(statement)

    def list_by_device(self, db: Session, device_id: UUID) -> list[InstalledSoftware]:
        statement = select(InstalledSoftware).where(InstalledSoftware.device_id == device_id)
        return list(db.scalars(statement).all())

    def list_by_user(self, db: Session, user_id: UUID) -> list[InstalledSoftware]:
        statement = select(InstalledSoftware).where(InstalledSoftware.user_id == user_id)
        return list(db.scalars(statement).all())

    def delete(self, db: Session, install: InstalledSoftware) -> None:
        db.delete(install)
        db.commit()


class InstallationRequestRepository:
    def create(self, db: Session, request: InstallationRequest) -> InstallationRequest:
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    def get_by_id(self, db: Session, request_id: UUID) -> InstallationRequest | None:
        statement = select(InstallationRequest).where(InstallationRequest.id == request_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        status: InstallationRequestStatus | None = None,
        user_id: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[InstallationRequest]:
        statement = select(InstallationRequest)

        if status:
            statement = statement.where(InstallationRequest.status == status)
        if user_id:
            statement = statement.where(InstallationRequest.user_id == user_id)

        statement = (
            statement.order_by(desc(InstallationRequest.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def save(self, db: Session, request: InstallationRequest) -> InstallationRequest:
        db.commit()
        db.refresh(request)
        return request