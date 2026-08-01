import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.access.enums import AccessRequestStatus, AccessRequestType


class AccessRequest(TenantBase):
    __tablename__ = "access_requests"

    __table_args__ = (
        Index("ix_access_requests_requested_by", "requested_by"),
        Index("ix_access_requests_status", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_type: Mapped[AccessRequestType] = mapped_column(
        SqlEnum(AccessRequestType),
        nullable=False,
    )

    target_resource: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    requested_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    status: Mapped[AccessRequestStatus] = mapped_column(
        SqlEnum(AccessRequestStatus),
        default=AccessRequestStatus.PENDING,
        nullable=False,
    )

    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
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