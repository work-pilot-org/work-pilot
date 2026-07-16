import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateLicenseRequest(BaseModel):
    software_id: uuid.UUID | None = None
    license_key: str = Field(..., min_length=2, max_length=255)
    total_seats: int = Field(default=1, ge=1)
    expiry_date: datetime | None = None
    renewal_date: datetime | None = None


class UpdateLicenseRequest(BaseModel):
    software_id: uuid.UUID | None = None
    license_key: str | None = Field(default=None, min_length=2, max_length=255)
    total_seats: int | None = Field(default=None, ge=1)
    expiry_date: datetime | None = None
    renewal_date: datetime | None = None


class AssignLicenseRequest(BaseModel):
    assigned_to: uuid.UUID


class LicenseAssignmentResponse(BaseModel):
    id: uuid.UUID
    license_id: uuid.UUID
    assigned_to: uuid.UUID
    assigned_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class LicenseResponse(BaseModel):
    id: uuid.UUID
    software_id: uuid.UUID | None
    license_key: str
    total_seats: int
    used_seats: int
    expiry_date: datetime | None
    renewal_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )