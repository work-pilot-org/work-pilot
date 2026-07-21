from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


# =====================================================
# ENUMS
# =====================================================

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"


class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    RESIGNED = "RESIGNED"
    TERMINATED = "TERMINATED"


class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class MaritalStatus(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"


class DocumentType(str, Enum):
    AADHAAR = "AADHAAR"
    PAN = "PAN"
    PASSPORT = "PASSPORT"
    RESUME = "RESUME"
    OFFER_LETTER = "OFFER_LETTER"
    EXPERIENCE_CERTIFICATE = "EXPERIENCE_CERTIFICATE"
    OTHER = "OTHER"


# =====================================================
# EMPLOYEE
# =====================================================

class EmployeeCreate(BaseModel):
    auth_user_id: UUID

    employee_code: str = Field(..., min_length=1, max_length=30)

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

    phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None

    joining_date: date

    employment_type: EmploymentType
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE

    department_id: Optional[UUID] = None
    designation_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None

    work_location: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    profile_photo: Optional[str] = None


class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    first_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    last_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None

    joining_date: Optional[date] = None

    employment_type: Optional[EmploymentType] = None
    employment_status: Optional[EmploymentStatus] = None

    department_id: Optional[UUID] = None
    designation_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None

    work_location: Optional[str] = None
    profile_photo: Optional[str] = None

    is_active: Optional[bool] = None

    @model_validator(mode="after")
    def reject_explicit_nulls_for_required_fields(self):
        required_fields = {
            "employee_code",
            "first_name",
            "last_name",
            "joining_date",
            "employment_type",
            "employment_status",
            "is_active",
        }

        for field in required_fields:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null.")

        return self


class EmployeeResponse(BaseModel):
    id: UUID
    auth_user_id: UUID

    employee_code: str

    first_name: str
    last_name: str

    phone: Optional[str]
    gender: Optional[Gender]
    date_of_birth: Optional[date]

    joining_date: date

    employment_type: EmploymentType
    employment_status: EmploymentStatus

    department_id: Optional[UUID]
    designation_id: Optional[UUID]
    manager_id: Optional[UUID]

    work_location: Optional[str]
    profile_photo: Optional[str]

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# EMPLOYEE PROFILE
# =====================================================

class EmployeeProfileCreate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    emergency_contact_name: Optional[str] = None

    emergency_contact_phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    emergency_contact_relation: Optional[str] = None

    blood_group: Optional[BloodGroup] = None
    marital_status: Optional[MaritalStatus] = None


class EmployeeProfileUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    emergency_contact_name: Optional[str] = None

    emergency_contact_phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    emergency_contact_relation: Optional[str] = None

    blood_group: Optional[BloodGroup] = None
    marital_status: Optional[MaritalStatus] = None


class EmployeeProfileResponse(BaseModel):
    id: UUID
    employee_id: UUID

    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]

    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    emergency_contact_relation: Optional[str]

    blood_group: Optional[BloodGroup]
    marital_status: Optional[MaritalStatus]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# EMPLOYEE DOCUMENTS
# =====================================================

class EmployeeDocumentCreate(BaseModel):
    document_name: str = Field(..., max_length=150)
    document_type: DocumentType
    file_url: str


class EmployeeDocumentResponse(BaseModel):
    id: UUID
    employee_id: UUID

    document_name: str
    document_type: DocumentType
    file_url: str

    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# SEARCH
# =====================================================

class EmployeeSearch(BaseModel):
    keyword: Optional[str] = None

    department_id: Optional[UUID] = None
    designation_id: Optional[UUID] = None

    employment_status: Optional[EmploymentStatus] = None

    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)

    sort_by: str = "created_at"
    sort_order: str = "desc"


# =====================================================
# LIST RESPONSE
# =====================================================

class EmployeeListResponse(BaseModel):
    total: int
    page: int
    size: int

    items: list[EmployeeResponse]


# =====================================================
# COMPLETE EMPLOYEE RESPONSE
# =====================================================

class EmployeeCompleteResponse(EmployeeResponse):
    profile: Optional[EmployeeProfileResponse] = None
    documents: list[EmployeeDocumentResponse] = Field(default_factory=list)
