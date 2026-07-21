import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.devices.enums import DeviceStatus


class Device(TenantBase):
    __tablename__ = "devices"

    __table_args__ = (
        Index("ix_devices_assigned_to", "assigned_to"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[DeviceStatus] = mapped_column(
        SqlEnum(DeviceStatus),
        default=DeviceStatus.ACTIVE,
        nullable=False,
    )

    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
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

    maintenance_history = relationship(
        "DeviceMaintenanceHistory",
        back_populates="device",
        cascade="all, delete-orphan",
    )


class DeviceMaintenanceHistory(TenantBase):
    __tablename__ = "device_maintenance_history"

    __table_args__ = (
        Index("ix_device_maintenance_device_id", "device_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    maintenance_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    performed_by: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
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

    device: Mapped["Device"] = relationship(
        "Device",
        back_populates="maintenance_history",
    )