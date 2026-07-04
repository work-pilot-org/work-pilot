from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TenantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class TenantCreate(BaseModel):
    company_name: str
    schema_name: str


class DomainCreate(BaseModel):
    domain: str
    is_primary: bool = True


class TenantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str
    schema_name: str
    status: TenantStatus
    created_at: datetime


class DomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    is_primary: bool