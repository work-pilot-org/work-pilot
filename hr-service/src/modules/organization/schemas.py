from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr


class DepartmentBase(BaseModel):
    name: str
    description: str | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DesignationBase(BaseModel):
    name: str
    description: str | None = None
    department_id: int | None = None


class DesignationCreate(DesignationBase):
    pass


class DesignationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    department_id: int | None = None
    is_active: bool | None = None


class DesignationResponse(DesignationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BranchBase(BaseModel):
    name: str
    code: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    phone: str | None = None
    email: EmailStr | None = None


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class BranchResponse(BranchBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    grace_time: int = 0
    is_night_shift: bool = False


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    name: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    grace_time: int | None = None
    is_night_shift: bool | None = None
    is_active: bool | None = None


class ShiftResponse(ShiftBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)            