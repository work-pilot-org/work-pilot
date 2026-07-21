import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.software.enums import InstallationRequestStatus
from it_service.modules.software.repository import (
    InstallationRequestRepository,
    InstalledSoftwareRepository,
    SoftwareRepository,
)
from it_service.modules.software.schemas import (
    CreateInstallationRequest,
    CreateInstallRequest,
    CreateSoftwareRequest,
    InstallationRequestResponse,
    InstalledSoftwareResponse,
    SoftwareResponse,
   
    UpdateSoftwareRequest,
)
from it_service.modules.software.service import SoftwareService

router = APIRouter(
    prefix="/software",
    tags=["Software"],
)


def get_software_service() -> SoftwareService:
    return SoftwareService(
        repository=SoftwareRepository(),
        installed_repository=InstalledSoftwareRepository(),
        request_repository=InstallationRequestRepository(),
    )


# Catalog CRUD
@router.post("", response_model=SoftwareResponse, status_code=status.HTTP_201_CREATED)
def create_software(
    payload: CreateSoftwareRequest,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.create_software(db, payload)


@router.get("", response_model=list[SoftwareResponse])
def list_software(
    search: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.list_software(db, search=search, skip=skip, limit=limit)


@router.get("/{software_id}", response_model=SoftwareResponse)
def get_software(
    software_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.get_software(db, software_id)


@router.put("/{software_id}", response_model=SoftwareResponse)
def update_software(
    software_id: uuid.UUID,
    payload: UpdateSoftwareRequest,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.update_software(db, software_id, payload)


@router.delete("/{software_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_software(
    software_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    service.delete_software(db, software_id)


# Installations / Assignment
@router.post("/{software_id}/install", response_model=InstalledSoftwareResponse, status_code=status.HTTP_201_CREATED)
def install_software(
    software_id: uuid.UUID,
    payload: CreateInstallRequest,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.install_software(db, software_id, payload)


@router.delete("/installations/{install_id}", status_code=status.HTTP_204_NO_CONTENT)
def uninstall_software(
    install_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    service.uninstall_software(db, install_id)


@router.get("/installations/device/{device_id}", response_model=list[InstalledSoftwareResponse])
def list_device_installations(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.list_device_installations(db, device_id)


@router.get("/installations/user/{user_id}", response_model=list[InstalledSoftwareResponse])
def list_user_installations(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.list_user_installations(db, user_id)


# Installation Requests
@router.post("/requests", response_model=InstallationRequestResponse, status_code=status.HTTP_201_CREATED)
def create_installation_request(
    payload: CreateInstallationRequest,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.create_installation_request(db, payload)


@router.get("/requests", response_model=list[InstallationRequestResponse])
def list_installation_requests(
    status: InstallationRequestStatus | None = Query(None),
    user_id: uuid.UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.list_installation_requests(
        db, status=status, user_id=user_id, skip=skip, limit=limit
    )


@router.get("/requests/{request_id}", response_model=InstallationRequestResponse)
def get_installation_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: SoftwareService = Depends(get_software_service),
):
    return service.get_installation_request(db, request_id)


