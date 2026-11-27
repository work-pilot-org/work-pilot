import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.software.enums import InstallationRequestStatus
from it_service.modules.software.models import InstallationRequest, InstalledSoftware, Software
from it_service.modules.software.repository import (
    InstallationRequestRepository,
    InstalledSoftwareRepository,
    SoftwareRepository,
)
from it_service.modules.software.schemas import (
    CreateInstallationRequest,
    CreateInstallRequest,
    CreateSoftwareRequest,
    UpdateSoftwareRequest,
)


class SoftwareService:
    def __init__(
        self,
        repository: SoftwareRepository,
        installed_repository: InstalledSoftwareRepository,
        request_repository: InstallationRequestRepository,
    ):
        self.repository = repository
        self.installed_repository = installed_repository
        self.request_repository = request_repository

    def _get_software(self, db: Session, software_id: uuid.UUID) -> Software:
        software = self.repository.get_by_id(db, software_id)
        if not software:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Software not found.",
            )
        return software

    def create_software(self, db: Session, payload: CreateSoftwareRequest) -> Software:
        software = Software(
            name=payload.name,
            version=payload.version,
            publisher=payload.publisher,
            license_required=payload.license_required,
        )
        return self.repository.create(db, software)

    def get_software(self, db: Session, software_id: uuid.UUID) -> Software:
        return self._get_software(db, software_id)

    def list_software(self, db: Session, **filters) -> list[Software]:
        return self.repository.list(db, **filters)

    def update_software(
        self, db: Session, software_id: uuid.UUID, payload: UpdateSoftwareRequest
    ) -> Software:
        software = self._get_software(db, software_id)
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(software, field, value)
        return self.repository.save(db, software)

    def delete_software(self, db: Session, software_id: uuid.UUID) -> None:
        software = self._get_software(db, software_id)
        self.repository.delete(db, software)

    # Installed Software / Software Assignment
    def install_software(
        self, db: Session, software_id: uuid.UUID, payload: CreateInstallRequest
    ) -> InstalledSoftware:
        self._get_software(db, software_id)
        
        if not payload.device_id and not payload.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must specify either device_id or user_id for software installation.",
            )
            
        if payload.device_id:
            existing = self.installed_repository.get_by_software_and_device(
                db, software_id, payload.device_id
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Software is already installed on this device.",
                )

        if payload.user_id:
            existing = self.installed_repository.get_by_software_and_user(
                db, software_id, payload.user_id
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Software is already assigned to this user.",
                )

        install = InstalledSoftware(
            software_id=software_id,
            device_id=payload.device_id,
            user_id=payload.user_id,
        )
        return self.installed_repository.create(db, install)

    def uninstall_software(self, db: Session, install_id: uuid.UUID) -> None:
        install = self.installed_repository.get_by_id(db, install_id)
        if not install:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Installation record not found.",
            )
        self.installed_repository.delete(db, install)

    def list_device_installations(self, db: Session, device_id: uuid.UUID) -> list[InstalledSoftware]:
        return self.installed_repository.list_by_device(db, device_id)

    def list_user_installations(self, db: Session, user_id: uuid.UUID) -> list[InstalledSoftware]:
        return self.installed_repository.list_by_user(db, user_id)

    # Installation Requests
    def create_installation_request(
        self, db: Session, payload: CreateInstallationRequest
    ) -> InstallationRequest:
        self._get_software(db, payload.software_id)
        request = InstallationRequest(
            software_id=payload.software_id,
            user_id=payload.user_id,
            reason=payload.reason,
            status=InstallationRequestStatus.PENDING,
        )
        return self.request_repository.create(db, request)

    def get_installation_request(self, db: Session, request_id: uuid.UUID) -> InstallationRequest:
        request = self.request_repository.get_by_id(db, request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Installation request not found.",
            )
        return request

    def list_installation_requests(self, db: Session, **filters) -> list[InstallationRequest]:
        return self.request_repository.list(db, **filters)

    