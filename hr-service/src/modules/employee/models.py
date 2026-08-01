import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import TenantBase


class Employee(TenantBase):
    __tablename__ = "employees"
    __table_args__ = (
        Index(
            "uq_employees_auth_user_id_active",
            "auth_user_id",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
        Index(
            "uq_employees_employee_code_active",
            "employee_code",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # User ID from Auth Service
    auth_user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    employee_code = Column(
        String(30),
        nullable=False,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=False,
    )

    phone = Column(String(20))

    gender = Column(String(20))

    date_of_birth = Column(Date)

    joining_date = Column(
        Date,
        nullable=False,
    )

    employment_type = Column(
        String(50),
        nullable=False,
    )

    employment_status = Column(
        String(50),
        nullable=False,
        default="ACTIVE",
    )

    department_id = Column(
        UUID(as_uuid=True),
        nullable=True,
    )

    designation_id = Column(
        UUID(as_uuid=True),
        nullable=True,
    )

    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id"),
        nullable=True,
    )

    work_location = Column(
        String(150),
    )

    profile_photo = Column(Text)

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    manager = relationship(
        "Employee",
        remote_side=[id],
        backref="subordinates",
    )

    profile = relationship(
        "EmployeeProfile",
        uselist=False,
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "EmployeeDocument",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    attendance_records = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    leave_requests = relationship(
        "LeaveRequest",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    leave_balances = relationship(
        "LeaveBalance",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


class EmployeeProfile(TenantBase):
    __tablename__ = "employee_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    address = Column(Text)

    city = Column(String(100))

    state = Column(String(100))

    country = Column(String(100))

    postal_code = Column(String(20))

    emergency_contact_name = Column(String(100))

    emergency_contact_phone = Column(String(20))

    emergency_contact_relation = Column(String(50))

    blood_group = Column(String(10))

    marital_status = Column(String(30))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    employee = relationship(
        "Employee",
        back_populates="profile",
    )


class EmployeeDocument(TenantBase):
    __tablename__ = "employee_documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    document_name = Column(
        String(150),
        nullable=False,
    )

    document_type = Column(
        String(100),
    )

    file_url = Column(
        Text,
        nullable=False,
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    employee = relationship(
        "Employee",
        back_populates="documents",
    )
