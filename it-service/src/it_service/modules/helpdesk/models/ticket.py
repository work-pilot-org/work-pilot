import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from it_service.infrastructure.database.base import TenantBase
from it_service.modules.helpdesk.enums import (
    TicketCategory,
    TicketPriority,
    TicketResolution,
    TicketSource,
    TicketStatus,
)


class Ticket(TenantBase):
    """
    Represents an IT Help Desk support ticket.
    """

    __tablename__ = "tickets"

    __table_args__ = (
        Index("ix_ticket_ticket_number", "ticket_number"),
        Index("ix_ticket_status", "status"),
        Index("ix_ticket_priority", "priority"),
        Index("ix_ticket_requester", "requester_id"),
        Index("ix_ticket_assigned_to", "assigned_to"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ticket_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[TicketCategory] = mapped_column(
        SqlEnum(TicketCategory),
        nullable=False,
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SqlEnum(TicketPriority),
        default=TicketPriority.MEDIUM,
        nullable=False,
    )

    status: Mapped[TicketStatus] = mapped_column(
        SqlEnum(TicketStatus),
        default=TicketStatus.OPEN,
        nullable=False,
    )

    source: Mapped[TicketSource] = mapped_column(
        SqlEnum(TicketSource),
        default=TicketSource.WEB,
        nullable=False,
    )

    requester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    resolution: Mapped[TicketResolution | None] = mapped_column(
        SqlEnum(TicketResolution),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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

    comments = relationship(
        "TicketComment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    attachments = relationship(
        "TicketAttachment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    activities = relationship(
        "TicketActivity",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )