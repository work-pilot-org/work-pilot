import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from it_service.modules.helpdesk.models.ticket import Ticket

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from it_service.infrastructure.database.base import TenantBase


class CommentType(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"


class TicketComment(TenantBase):
    """
    Stores comments associated with a help desk ticket.
    """

    __tablename__ = "ticket_comments"

    __table_args__ = (
        Index("ix_ticket_comments_ticket_id", "ticket_id"),
        Index("ix_ticket_comments_author_id", "author_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    comment_type: Mapped[CommentType] = mapped_column(
        SqlEnum(CommentType),
        default=CommentType.PUBLIC,
        nullable=False,
    )

    is_edited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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

    ticket: Mapped["Ticket"] = relationship(
        "Ticket",
        back_populates="comments",
    )