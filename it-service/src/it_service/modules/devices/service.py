import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.devices.enums import DeviceStatus
from it_service.modules.devices.models import Device, DeviceMaintenanceHistory
from it_service.modules.devices.repository import (
    DeviceMaintenanceHistoryRepository,
    DeviceRepository,
)
from it_service.modules.devices.schemas import (
    AssignDeviceRequest,
    CreateDeviceRequest,
    CreateMaintenanceHistoryRequest,
    UpdateDeviceRequest,
)


class DeviceService:
    def __init__(
        self,
        repository: DeviceRepository,
        maintenance_repository: DeviceMaintenanceHistoryRepository,
    ):
        self.repository = repository
        self.maintenance_repository = maintenance_repository

    def _get_device(self, db: Session, device_id: uuid.UUID) -> Device:
        device = self.repository.get_by_id(db, device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found.",
            )
        return device

    def create_device(self, db: Session, payload: CreateDeviceRequest) -> Device:
        device = Device(
            name=payload.name,
            model=payload.model,
            status=payload.status,
        )
        return self.repository.create(db, device)

    def get_device(self, db: Session, device_id: uuid.UUID) -> Device:
        return self._get_device(db, device_id)

    def list_devices(self, db: Session, **filters) -> list[Device]:
        return self.repository.list(db, **filters)

    def update_device(
        self, db: Session, device_id: uuid.UUID, payload: UpdateDeviceRequest
    ) -> Device:
        device = self._get_device(db, device_id)
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(device, field, value)
        return self.repository.save(db, device)

    def assign_device(
        self, db: Session, device_id: uuid.UUID, payload: AssignDeviceRequest
    ) -> Device:
        device = self._get_device(db, device_id)
        if device.status != DeviceStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device is not active. Current status: {device.status.value}",
            )
        device.assigned_to = payload.assigned_to
        return self.repository.save(db, device)

    def return_device(self, db: Session, device_id: uuid.UUID) -> Device:
        device = self._get_device(db, device_id)
        device.assigned_to = None
        return self.repository.save(db, device)

    def delete_device(self, db: Session, device_id: uuid.UUID) -> None:
        device = self._get_device(db, device_id)
        self.repository.delete(db, device)

    def add_maintenance_log(
        self,
        db: Session,
        device_id: uuid.UUID,
        payload: CreateMaintenanceHistoryRequest,
    ) -> DeviceMaintenanceHistory:
        # Verify device exists
        self._get_device(db, device_id)
        
        maintenance = DeviceMaintenanceHistory(
            device_id=device_id,
            description=payload.description,
            performed_by=payload.performed_by,
            cost=payload.cost,
            maintenance_date=payload.maintenance_date or datetime.utcnow(),
        )
        return self.maintenance_repository.create(db, maintenance)

    def get_maintenance_history(
        self, db: Session, device_id: uuid.UUID
    ) -> list[DeviceMaintenanceHistory]:
        # Verify device exists
        self._get_device(db, device_id)
        return self.maintenance_repository.list_by_device(db, device_id)