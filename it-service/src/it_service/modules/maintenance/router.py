import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.maintenance.enums import MaintenanceStatus, MaintenanceType
from it_service.modules.maintenance.repository import MaintenanceRepository
from it_service.modules.maintenance.schemas import (
    CompleteMaintenanceRequest,
    CreateMaintenanceRecord,
    MaintenanceRecordResponse,
    UpdateMaintenanceRecord,
)
from it_service.modules.maintenance.service import MaintenanceService

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


def get_maintenance_service() -> MaintenanceService:
    return MaintenanceService(repository=MaintenanceRepository())


@router.post("", response_model=MaintenanceRecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    payload: CreateMaintenanceRecord,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.create_record(db, payload)


@router.get("", response_model=list[MaintenanceRecordResponse])
def list_records(
    device_id: uuid.UUID | None = Query(None),
    maintenance_type: MaintenanceType | None = Query(None),
    status: MaintenanceStatus | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.list_records(
        db,
        device_id=device_id,
        maintenance_type=maintenance_type,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.get("/{record_id}", response_model=MaintenanceRecordResponse)
def get_record(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.get_record(db, record_id)


@router.put("/{record_id}", response_model=MaintenanceRecordResponse)
def update_record(
    record_id: uuid.UUID,
    payload: UpdateMaintenanceRecord,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.update_record(db, record_id, payload)


@router.post("/{record_id}/start", response_model=MaintenanceRecordResponse)
def start_maintenance(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.start_maintenance(db, record_id)


@router.post("/{record_id}/complete", response_model=MaintenanceRecordResponse)
def complete_maintenance(
    record_id: uuid.UUID,
    payload: CompleteMaintenanceRequest,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.complete_maintenance(db, record_id, payload)


@router.post("/{record_id}/cancel", response_model=MaintenanceRecordResponse)
def cancel_maintenance(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    return service.cancel_maintenance(db, record_id)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    service.delete_record(db, record_id)