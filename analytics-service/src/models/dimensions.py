from sqlalchemy import BigInteger, Boolean, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import TenantBase


class DimTenant(TenantBase):
    __tablename__ = "dim_tenant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, index=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class DimDate(TenantBase):
    __tablename__ = "dim_date"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Usually YYYYMMDD as integer
    date: Mapped[Date] = mapped_column(Date, unique=True, nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    is_weekend: Mapped[bool] = mapped_column(Boolean, nullable=False)


class DimEmployee(TenantBase):
    __tablename__ = "dim_employee"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    employment_type: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class DimDepartment(TenantBase):
    __tablename__ = "dim_department"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    department_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class DimDesignation(TenantBase):
    __tablename__ = "dim_designation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    designation_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=True)


class DimBranch(TenantBase):
    __tablename__ = "dim_branch"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    branch_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)


class DimAsset(TenantBase):
    __tablename__ = "dim_asset"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    asset_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False, default="Unknown")
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class DimDevice(TenantBase):
    __tablename__ = "dim_device"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    device_type: Mapped[str] = mapped_column(String(100), nullable=True)
    os: Mapped[str] = mapped_column(String(100), nullable=True)
    model: Mapped[str] = mapped_column(String(150), nullable=False)


class DimSoftware(TenantBase):
    __tablename__ = "dim_software"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    software_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    publisher: Mapped[str] = mapped_column(String(150), nullable=True)


class DimLicense(TenantBase):
    __tablename__ = "dim_license"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    license_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    license_type: Mapped[str] = mapped_column(String(100), nullable=False)


class DimWorkflow(TenantBase):
    __tablename__ = "dim_workflow"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    workflow_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    workflow_type: Mapped[str] = mapped_column(String(100), nullable=False)
