import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.assets.enums import AssetCategory, AssetStatus


class CreateAssetRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    serial_number: str = Field(..., min_length=2, max_length=100)
    category: AssetCategory
    status: AssetStatus = AssetStatus.AVAILABLE


class UpdateAssetRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    category: AssetCategory | None = None
    status: AssetStatus | None = None


class AssignAssetRequest(BaseModel):
    assigned_to: uuid.UUID


class AssetResponse(BaseModel):
    id: uuid.UUID
    name: str
    serial_number: str
    category: AssetCategory
    status: AssetStatus
    assigned_to: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )