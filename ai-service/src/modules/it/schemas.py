"""
Schemas for the IT Agent.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Help Desk Enums
# ==========================================================

class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# ==========================================================
# Help Desk Schemas
# ==========================================================

class CreateTicketRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=5)
    priority: TicketPriority = TicketPriority.MEDIUM


class UpdateTicketRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None


class AssignTicketRequest(BaseModel):
    assignee_id: uuid.UUID


class TicketResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    assignee_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Asset Enums
# ==========================================================

class AssetCategory(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    MONITOR = "MONITOR"
    MOBILE = "MOBILE"
    ACCESSORY = "ACCESSORY"
    OTHER = "OTHER"


class AssetStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"


# ==========================================================
# Asset Schemas
# ==========================================================

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
    assigned_to: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    
# ==========================================================
# Device Enums
# ==========================================================

class DeviceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"


# ==========================================================
# Device Schemas
# ==========================================================

class CreateDeviceRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    model: str = Field(..., min_length=2, max_length=100)
    status: DeviceStatus = DeviceStatus.ACTIVE


class UpdateDeviceRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    model: str | None = Field(default=None, min_length=2, max_length=100)
    status: DeviceStatus | None = None


class AssignDeviceRequest(BaseModel):
    assigned_to: uuid.UUID


class CreateMaintenanceHistoryRequest(BaseModel):
    description: str = Field(..., min_length=5, max_length=1000)
    performed_by: str = Field(..., min_length=2, max_length=150)
    cost: float | None = None
    maintenance_date: datetime | None = None


class MaintenanceHistoryResponse(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    maintenance_date: datetime
    description: str
    performed_by: str
    cost: float | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceResponse(BaseModel):
    id: uuid.UUID
    name: str
    model: str
    status: DeviceStatus
    assigned_to: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# ==========================================================
# Software Enums
# ==========================================================

class InstallationRequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    INSTALLED = "INSTALLED"


# ==========================================================
# Software Schemas
# ==========================================================

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

    model_config = ConfigDict(from_attributes=True)


class CreateInstallRequest(BaseModel):
    device_id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None


class InstalledSoftwareResponse(BaseModel):
    id: uuid.UUID
    software_id: uuid.UUID
    device_id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    installed_at: datetime

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)
    
# ==========================================================
# License Schemas
# ==========================================================

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

    model_config = ConfigDict(from_attributes=True)


class LicenseResponse(BaseModel):
    id: uuid.UUID
    software_id: uuid.UUID | None = None
    license_key: str
    total_seats: int
    used_seats: int
    expiry_date: datetime | None = None
    renewal_date: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# ==========================================================
# Access Enums
# ==========================================================

class AccessRequestType(str, Enum):
    # Copy the exact values from the IT Service enum
    ...


class AccessRequestStatus(str, Enum):
    # Copy the exact values from the IT Service enum
    ...


# ==========================================================
# Access Schemas
# ==========================================================

class CreateAccessRequest(BaseModel):
    request_type: AccessRequestType
    target_resource: str = Field(..., min_length=2, max_length=255)
    requested_by: uuid.UUID
    reason: str | None = Field(default=None, max_length=1000)


class UpdateAccessRequest(BaseModel):
    target_resource: str | None = Field(default=None, min_length=2, max_length=255)
    reason: str | None = None


class AccessRequestStatusUpdate(BaseModel):
    status: AccessRequestStatus


class AccessRequestResponse(BaseModel):
    id: uuid.UUID
    request_type: AccessRequestType
    target_resource: str
    requested_by: uuid.UUID
    status: AccessRequestStatus
    approved_by: uuid.UUID | None = None
    reason: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# ==========================================================
# Maintenance Enums
# ==========================================================

class MaintenanceType(str, Enum):
    # Copy the exact enum values from the IT Service
    ...


class MaintenanceStatus(str, Enum):
    # Copy the exact enum values from the IT Service
    ...


# ==========================================================
# Maintenance Schemas
# ==========================================================

class CreateMaintenanceRecord(BaseModel):
    device_id: uuid.UUID | None = None
    maintenance_type: MaintenanceType
    description: str = Field(..., min_length=5)
    vendor_name: str | None = Field(default=None, max_length=255)
    vendor_contact: str | None = Field(default=None, max_length=255)
    scheduled_date: datetime
    cost: float | None = None


class UpdateMaintenanceRecord(BaseModel):
    description: str | None = Field(default=None, min_length=5)
    vendor_name: str | None = Field(default=None, max_length=255)
    vendor_contact: str | None = Field(default=None, max_length=255)
    scheduled_date: datetime | None = None
    cost: float | None = None


class CompleteMaintenanceRequest(BaseModel):
    cost: float | None = None


class MaintenanceRecordResponse(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID | None = None
    maintenance_type: MaintenanceType
    description: str
    vendor_name: str | None = None
    vendor_contact: str | None = None
    status: MaintenanceStatus
    scheduled_date: datetime
    completed_date: datetime | None = None
    cost: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)