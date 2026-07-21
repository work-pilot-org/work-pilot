import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.access.enums import AccessRequestStatus, AccessRequestType


class CreateAccessRequest(BaseModel):
    request_type: AccessRequestType
    target_resource: str = Field(..., min_length=2, max_length=255)
    requested_by: uuid.UUID
    reason: str | None = None


class UpdateAccessRequest(BaseModel):
    target_resource: str | None = Field(default=None, min_length=2, max_length=255)
    reason: str | None = None




class AccessRequestResponse(BaseModel):
    id: uuid.UUID
    request_type: AccessRequestType
    target_resource: str
    requested_by: uuid.UUID
    status: AccessRequestStatus
    approved_by: uuid.UUID | None
    reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )