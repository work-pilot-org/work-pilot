import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.maintenance.enums import MaintenanceStatus, MaintenanceType


class CreateMaintenanceRecord(BaseModel):
    device_id: uuid.UUID | None = None
    maintenance_type: MaintenanceType
    description: str = Field(..., min_length=5)
    vendor_name: str | None = Field(default=None, max_length=255)
    vendor_contact: str | None = Field(default=None, max_length=255)
    scheduled_date: datetime
    cost: float | None = None


class UpdateMaintenanceRecord(BaseModel):
    description: str | None = Field(default=None, min_length=5)
    vendor_name: str | None = Field(default=None, max_length=255)
    vendor_contact: str | None = Field(default=None, max_length=255)
    scheduled_date: datetime | None = None
    cost: float | None = None


class CompleteMaintenanceRequest(BaseModel):
    cost: float | None = None


class MaintenanceRecordResponse(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID | None
    maintenance_type: MaintenanceType
    description: str
    vendor_name: str | None
    vendor_contact: str | None
    status: MaintenanceStatus
    scheduled_date: datetime
    completed_date: datetime | None
    cost: float | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )