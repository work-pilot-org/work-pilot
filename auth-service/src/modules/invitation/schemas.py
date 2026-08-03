from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

from src.modules.employee.models import Role
from src.modules.invitation.models import InvitationStatus


class InvitationCreateRequest(BaseModel):
    email: EmailStr
    role: Role = Field(default=Role.EMPLOYEE)

    @validator('email')
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class InvitationResponse(BaseModel):
    id: UUID
    tenant_id: int
    email: str
    role: Role
    status: InvitationStatus
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    accepted_by_user_id: Optional[UUID]
    revoked_at: Optional[datetime]
    last_sent_at: Optional[datetime]

    class Config:
        orm_mode = True


class InvitationValidateResponse(BaseModel):
    valid: bool
    expired: bool
    revoked: bool
    company_name: Optional[str] = None
    role: Optional[Role] = None
    user_exists: bool
    email: Optional[str] = None


class AcceptInvitationRequest(BaseModel):
    token: str = Field(..., min_length=32)
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator('password')
    def validate_complexity(cls, v):
        from shared_infrastructure.core.security import validate_password_complexity
        return validate_password_complexity(v)

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
