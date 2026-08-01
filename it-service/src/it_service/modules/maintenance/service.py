import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.maintenance.enums import MaintenanceStatus
from it_service.modules.maintenance.models import MaintenanceRecord
from it_service.modules.maintenance.repository import MaintenanceRepository
from it_service.modules.maintenance.schemas import (
    CompleteMaintenanceRequest,
    CreateMaintenanceRecord,
    UpdateMaintenanceRecord,
)


class MaintenanceService:
    def __init__(self, repository: MaintenanceRepository):
        self.repository = repository

    def _get_record(self, db: Session, record_id: uuid.UUID) -> MaintenanceRecord:
        record = self.repository.get_by_id(db, record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found.",
            )
        return record

    def create_record(self, db: Session, payload: CreateMaintenanceRecord) -> MaintenanceRecord:
        record = MaintenanceRecord(
            device_id=payload.device_id,
            maintenance_type=payload.maintenance_type,
            description=payload.description,
            vendor_name=payload.vendor_name,
            vendor_contact=payload.vendor_contact,
            scheduled_date=payload.scheduled_date,
            cost=payload.cost,
            status=MaintenanceStatus.PENDING,
        )
        return self.repository.create(db, record)

    def get_record(self, db: Session, record_id: uuid.UUID) -> MaintenanceRecord:
        return self._get_record(db, record_id)

    def list_records(self, db: Session, **filters) -> list[MaintenanceRecord]:
        return self.repository.list(db, **filters)

    def update_record(
        self, db: Session, record_id: uuid.UUID, payload: UpdateMaintenanceRecord
    ) -> MaintenanceRecord:
        record = self._get_record(db, record_id)
        if record.status in (MaintenanceStatus.COMPLETED, MaintenanceStatus.CANCELLED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update record in {record.status.value} status.",
            )

        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(record, field, value)
            
        return self.repository.save(db, record)

    def start_maintenance(self, db: Session, record_id: uuid.UUID) -> MaintenanceRecord:
        record = self._get_record(db, record_id)
        if record.status != MaintenanceStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot start maintenance from status: {record.status.value}",
            )
        record.status = MaintenanceStatus.IN_PROGRESS
        return self.repository.save(db, record)

    def complete_maintenance(
        self, db: Session, record_id: uuid.UUID, payload: CompleteMaintenanceRequest
    ) -> MaintenanceRecord:
        record = self._get_record(db, record_id)
        if record.status not in (MaintenanceStatus.PENDING, MaintenanceStatus.IN_PROGRESS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot complete maintenance from status: {record.status.value}",
            )
        
        record.status = MaintenanceStatus.COMPLETED
        record.completed_date = datetime.utcnow()
        if payload.cost is not None:
            record.cost = payload.cost

        return self.repository.save(db, record)

    def cancel_maintenance(self, db: Session, record_id: uuid.UUID) -> MaintenanceRecord:
        record = self._get_record(db, record_id)
        if record.status in (MaintenanceStatus.COMPLETED, MaintenanceStatus.CANCELLED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel maintenance from status: {record.status.value}",
            )
        
        record.status = MaintenanceStatus.CANCELLED
        return self.repository.save(db, record)

    def delete_record(self, db: Session, record_id: uuid.UUID) -> None:
        record = self._get_record(db, record_id)
        self.repository.delete(db, record)