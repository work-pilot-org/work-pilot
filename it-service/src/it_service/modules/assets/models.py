import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.assets.enums import AssetCategory, AssetStatus


class Asset(TenantBase):
    __tablename__ = "assets"

    __table_args__ = (
        Index("ix_assets_serial_number", "serial_number"),
        Index("ix_assets_assigned_to", "assigned_to"),
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

    serial_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    category: Mapped[AssetCategory] = mapped_column(
        SqlEnum(AssetCategory),
        nullable=False,
    )

    status: Mapped[AssetStatus] = mapped_column(
        SqlEnum(AssetStatus),
        default=AssetStatus.AVAILABLE,
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