import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.software.enums import InstallationRequestStatus


class Software(TenantBase):
    __tablename__ = "software"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    publisher: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    license_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    installations = relationship(
        "InstalledSoftware",
        back_populates="software",
        cascade="all, delete-orphan",
    )

    requests = relationship(
        "InstallationRequest",
        back_populates="software",
        cascade="all, delete-orphan",
    )


class InstalledSoftware(TenantBase):
    __tablename__ = "installed_software"

    __table_args__ = (
        Index("ix_installed_software_software_id", "software_id"),
        Index("ix_installed_software_device_id", "device_id"),
        Index("ix_installed_software_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    software_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("software.id", ondelete="CASCADE"),
        nullable=False,
    )

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    installed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    software: Mapped["Software"] = relationship(
        "Software",
        back_populates="installations",
    )


class InstallationRequest(TenantBase):
    __tablename__ = "software_installation_requests"

    __table_args__ = (
        Index("ix_install_req_software_id", "software_id"),
        Index("ix_install_req_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    software_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("software.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[InstallationRequestStatus] = mapped_column(
        SqlEnum(InstallationRequestStatus),
        default=InstallationRequestStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    software: Mapped["Software"] = relationship(
        "Software",
        back_populates="requests",
    )