from datetime import date, datetime
from enum import Enum
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

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    gender: Gender | None = None
    date_of_birth: date | None = None

    joining_date: date

    employment_type: EmploymentType
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE

    department_id: UUID | None = None
    designation_id: UUID | None = None
    manager_id: UUID | None = None

    work_location: str | None = Field(
        default=None,
        max_length=150,
    )

    profile_photo: str | None = None


class EmployeeUpdate(BaseModel):
    employee_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    gender: Gender | None = None
    date_of_birth: date | None = None

    joining_date: date | None = None

    employment_type: EmploymentType | None = None
    employment_status: EmploymentStatus | None = None

    department_id: UUID | None = None
    designation_id: UUID | None = None
    manager_id: UUID | None = None

    work_location: str | None = None
    profile_photo: str | None = None

    is_active: bool | None = None

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

    phone: str | None
    gender: Gender | None
    date_of_birth: date | None

    joining_date: date

    employment_type: EmploymentType
    employment_status: EmploymentStatus

    department_id: UUID | None
    designation_id: UUID | None
    manager_id: UUID | None

    work_location: str | None
    profile_photo: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# EMPLOYEE PROFILE
# =====================================================

class EmployeeProfileCreate(BaseModel):
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None

    emergency_contact_name: str | None = None

    emergency_contact_phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    emergency_contact_relation: str | None = None

    blood_group: BloodGroup | None = None
    marital_status: MaritalStatus | None = None


class EmployeeProfileUpdate(BaseModel):
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None

    emergency_contact_name: str | None = None

    emergency_contact_phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15,
    )

    emergency_contact_relation: str | None = None

    blood_group: BloodGroup | None = None
    marital_status: MaritalStatus | None = None


class EmployeeProfileResponse(BaseModel):
    id: UUID
    employee_id: UUID

    address: str | None
    city: str | None
    state: str | None
    country: str | None
    postal_code: str | None

    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    emergency_contact_relation: str | None

    blood_group: BloodGroup | None
    marital_status: MaritalStatus | None

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
    keyword: str | None = None

    department_id: UUID | None = None
    designation_id: UUID | None = None

    employment_status: EmploymentStatus | None = None

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
    profile: EmployeeProfileResponse | None = None
    documents: list[EmployeeDocumentResponse] = Field(default_factory=list)
