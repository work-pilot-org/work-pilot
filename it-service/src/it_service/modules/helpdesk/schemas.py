import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from it_service.modules.helpdesk.enums import (
    TicketCategory,
    TicketPriority,
    TicketResolution,
    TicketSource,
    TicketStatus,
)
from it_service.modules.helpdesk.models.ticket_comment import CommentType

# ==========================================================
# Ticket Request Schemas
# ==========================================================

class CreateTicketRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=150)
    description: str = Field(..., min_length=10)
    category: TicketCategory
    priority: TicketPriority = TicketPriority.MEDIUM
    source: TicketSource = TicketSource.WEB


class UpdateTicketRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=5,
        max_length=150,
    )
    description: str | None = None
    category: TicketCategory | None = None
    priority: TicketPriority | None = None


class UpdateTicketStatusRequest(BaseModel):
    status: TicketStatus
    resolution: TicketResolution | None = None


class AssignTicketRequest(BaseModel):
    assigned_to: uuid.UUID


# ==========================================================
# Comment Request Schemas
# ==========================================================

class CreateCommentRequest(BaseModel):
    comment: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    comment_type: CommentType = CommentType.PUBLIC


class UpdateCommentRequest(BaseModel):
    comment: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


# ==========================================================
# Ticket Response
# ==========================================================

class TicketResponse(BaseModel):
    id: uuid.UUID
    ticket_number: str

    title: str
    description: str

    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    source: TicketSource

    requester_id: uuid.UUID
    assigned_to: uuid.UUID | None

    resolution: TicketResolution | None

    resolved_at: datetime | None
    closed_at: datetime | None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Comment Response
# ==========================================================

class CommentResponse(BaseModel):
    id: uuid.UUID

    ticket_id: uuid.UUID

    author_id: uuid.UUID

    comment: str

    comment_type: CommentType

    is_edited: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Attachment Response
# ==========================================================

class AttachmentResponse(BaseModel):
    id: uuid.UUID

    ticket_id: uuid.UUID

    file_name: str

    file_url: str

    file_type: str

    file_size: int

    uploaded_by: uuid.UUID

    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Activity Response
# ==========================================================

class ActivityResponse(BaseModel):
    id: uuid.UUID

    ticket_id: uuid.UUID

    action: str

    performed_by: uuid.UUID

    old_value: dict | None

    new_value: dict | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Ticket List Response
# ==========================================================

class TicketListResponse(BaseModel):
    total: int

    items: list[TicketResponse]


# ==========================================================
# Generic Response
# ==========================================================

class MessageResponse(BaseModel):
    message: str