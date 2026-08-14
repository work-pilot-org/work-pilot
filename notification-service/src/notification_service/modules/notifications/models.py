from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shared_infrastructure.database.base import TenantBase
from notification_service.modules.notifications.enums import (
    Channel,
    NotificationStatus,
    NotificationType,
)


class NotificationLog(TenantBase):
    __tablename__ = "notification_logs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    recipient_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    tenant_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    channel: Mapped[Channel] = mapped_column(
        Enum(Channel),
        nullable=False,
        default=Channel.EMAIL,
    )

    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus),
        nullable=False,
        default=NotificationStatus.PENDING,
        index=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
