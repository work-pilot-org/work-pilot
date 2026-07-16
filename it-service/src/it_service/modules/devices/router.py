import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.devices.enums import DeviceStatus
from it_service.modules.devices.repository import (
    DeviceMaintenanceHistoryRepository,
    DeviceRepository,
)
from it_service.modules.devices.schemas import (
    AssignDeviceRequest,
    CreateDeviceRequest,
    CreateMaintenanceHistoryRequest,
    DeviceResponse,
    MaintenanceHistoryResponse,
    UpdateDeviceRequest,
)
from it_service.modules.devices.service import DeviceService

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


def get_device_service() -> DeviceService:
    return DeviceService(
        repository=DeviceRepository(),
        maintenance_repository=DeviceMaintenanceHistoryRepository(),
    )


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    payload: CreateDeviceRequest,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.create_device(db, payload)


@router.get("", response_model=list[DeviceResponse])
def list_devices(
    status: DeviceStatus | None = Query(None),
    assigned_to: uuid.UUID | None = Query(None),
    search: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.list_devices(
        db,
        status=status,
        assigned_to=assigned_to,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.get_device(db, device_id)


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: uuid.UUID,
    payload: UpdateDeviceRequest,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.update_device(db, device_id, payload)


@router.post("/{device_id}/assign", response_model=DeviceResponse)
def assign_device(
    device_id: uuid.UUID,
    payload: AssignDeviceRequest,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.assign_device(db, device_id, payload)


@router.post("/{device_id}/return", response_model=DeviceResponse)
def return_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.return_device(db, device_id)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    service.delete_device(db, device_id)


# ==========================================================
# Maintenance History
# ==========================================================

@router.post("/{device_id}/maintenance", response_model=MaintenanceHistoryResponse, status_code=status.HTTP_201_CREATED)
def add_maintenance_log(
    device_id: uuid.UUID,
    payload: CreateMaintenanceHistoryRequest,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.add_maintenance_log(db, device_id, payload)


@router.get("/{device_id}/maintenance", response_model=list[MaintenanceHistoryResponse])
def get_maintenance_history(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: DeviceService = Depends(get_device_service),
):
    return service.get_maintenance_history(db, device_id)