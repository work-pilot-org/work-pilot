import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from it_service.infrastructure.database.base import TenantBase


class License(TenantBase):
    __tablename__ = "licenses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    software_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("software.id", ondelete="SET NULL"),
        nullable=True,
    )

    license_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    total_seats: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    used_seats: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    expiry_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    renewal_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    assignments = relationship(
        "LicenseAssignment",
        back_populates="license",
        cascade="all, delete-orphan",
    )


class LicenseAssignment(TenantBase):
    __tablename__ = "license_assignments"

    __table_args__ = (
        Index("ix_license_assignments_license_id", "license_id"),
        Index("ix_license_assignments_assigned_to", "assigned_to"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    license_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="CASCADE"),
        nullable=False,
    )

    assigned_to: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    license: Mapped["License"] = relationship(
        "License",
        back_populates="assignments",
    )