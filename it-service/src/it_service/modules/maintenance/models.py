import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Index, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.maintenance.enums import MaintenanceStatus, MaintenanceType


class MaintenanceRecord(TenantBase):
    __tablename__ = "maintenance_records"

    __table_args__ = (
        Index("ix_maintenance_records_device_id", "device_id"),
        Index("ix_maintenance_records_status", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    maintenance_type: Mapped[MaintenanceType] = mapped_column(
        SqlEnum(MaintenanceType),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    vendor_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    vendor_contact: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[MaintenanceStatus] = mapped_column(
        SqlEnum(MaintenanceStatus),
        default=MaintenanceStatus.PENDING,
        nullable=False,
    )

    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )