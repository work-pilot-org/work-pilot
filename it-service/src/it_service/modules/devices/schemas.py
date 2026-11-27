import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.devices.enums import DeviceStatus


class CreateDeviceRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    model: str = Field(..., min_length=2, max_length=100)
    status: DeviceStatus = DeviceStatus.ACTIVE


class UpdateDeviceRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    model: str | None = Field(default=None, min_length=2, max_length=100)
    status: DeviceStatus | None = None


class AssignDeviceRequest(BaseModel):
    assigned_to: uuid.UUID


class CreateMaintenanceHistoryRequest(BaseModel):
    description: str = Field(..., min_length=5, max_length=1000)
    performed_by: str = Field(..., min_length=2, max_length=150)
    cost: float | None = None
    maintenance_date: datetime | None = None


class MaintenanceHistoryResponse(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    maintenance_date: datetime
    description: str
    performed_by: str
    cost: float | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DeviceResponse(BaseModel):
    id: uuid.UUID
    name: str
    model: str
    status: DeviceStatus
    assigned_to: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )