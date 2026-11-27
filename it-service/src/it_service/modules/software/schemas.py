import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.software.enums import InstallationRequestStatus


class CreateSoftwareRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    version: str = Field(..., min_length=1, max_length=50)
    publisher: str = Field(..., min_length=2, max_length=150)
    license_required: bool = False


class UpdateSoftwareRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    version: str | None = Field(default=None, min_length=1, max_length=50)
    publisher: str | None = Field(default=None, min_length=2, max_length=150)
    license_required: bool | None = None


class SoftwareResponse(BaseModel):
    id: uuid.UUID
    name: str
    version: str
    publisher: str
    license_required: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateInstallRequest(BaseModel):
    device_id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None


class InstalledSoftwareResponse(BaseModel):
    id: uuid.UUID
    software_id: uuid.UUID
    device_id: uuid.UUID | None
    user_id: uuid.UUID | None
    installed_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateInstallationRequest(BaseModel):
    software_id: uuid.UUID
    user_id: uuid.UUID
    reason: str = Field(..., min_length=5, max_length=500)





class InstallationRequestResponse(BaseModel):
    id: uuid.UUID
    software_id: uuid.UUID
    user_id: uuid.UUID
    reason: str
    status: InstallationRequestStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )