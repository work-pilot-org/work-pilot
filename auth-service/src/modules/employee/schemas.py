from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Role(str, Enum):
    ORG_ADMIN = "ORG_ADMIN"
    HR_ADMIN = "HR_ADMIN"
    IT_ADMIN = "IT_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ON_LEAVE = "ON_LEAVE"
    TERMINATED = "TERMINATED"


class EmployeeCreate(BaseModel):
    user_id: UUID
    role: Role = Role.EMPLOYEE
    department: str | None = None
    job_title: str | None = None
    phone_number: str | None = None
    manager_id: UUID | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    role: Role
    department: str | None
    job_title: str | None
    phone_number: str | None
    manager_id: UUID | None
    employment_status: EmploymentStatus
    is_active: bool
    created_at: datetime