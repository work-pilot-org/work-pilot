import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.helpdesk.activity_repository import (
    TicketActivityRepository,
)
from it_service.modules.helpdesk.activity_service import (
    ActivityService,
)
from it_service.modules.helpdesk.comment_repository import (
    CommentRepository,
)
from it_service.modules.helpdesk.comment_service import (
    CommentService,
)
from it_service.modules.helpdesk.enums import (
    TicketPriority,
    TicketStatus,
)
from it_service.modules.helpdesk.repository import (
    TicketRepository,
)
from it_service.modules.helpdesk.schemas import (
    AssignTicketRequest,
    CommentResponse,
    CreateCommentRequest,
    CreateTicketRequest,
    MessageResponse,
    TicketResponse,
    UpdateCommentRequest,
    UpdateTicketRequest,
    UpdateTicketStatusRequest,
)
from it_service.modules.helpdesk.service import (
    TicketService,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Help Desk"],
)

# ==========================================================
# Dependency Injection
# ==========================================================


def get_ticket_service() -> TicketService:

    ticket_repository = TicketRepository()

    activity_repository = TicketActivityRepository()

    activity_service = ActivityService(
        activity_repository,
    )

    return TicketService(
        repository=ticket_repository,
        activity_service=activity_service,
    )


def get_comment_service() -> CommentService:

    comment_repository = CommentRepository()

    activity_repository = TicketActivityRepository()

    activity_service = ActivityService(
        activity_repository,
    )

    return CommentService(
        repository=comment_repository,
        activity_service=activity_service,
    )


TicketServiceDependency = Annotated[
    TicketService,
    Depends(get_ticket_service),
]

CommentServiceDependency = Annotated[
    CommentService,
    Depends(get_comment_service),
]

DatabaseDependency = Annotated[
    Session,
    Depends(get_db),
]

# ==========================================================
# Ticket Endpoints
# ==========================================================


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: CreateTicketRequest,
    request: Request,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Create ticket.
    """

    # TODO:
    # Replace with authenticated user
    requester_id = uuid.uuid4()

    return service.create_ticket(
        db=db,
        requester_id=requester_id,
        payload=payload,
    )


@router.get(
    "",
    response_model=list[TicketResponse],
)
def list_tickets(
    db: DatabaseDependency,
    service: TicketServiceDependency,
    status: TicketStatus | None = Query(None),
    priority: TicketPriority | None = Query(None),
    assigned_to: uuid.UUID | None = Query(None),
    search: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List tickets.
    """

    return service.list_tickets(
        db=db,
        status=status,
        priority=priority,
        assigned_to=assigned_to,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: uuid.UUID,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Get ticket.
    """

    return service.get_ticket(
        db=db,
        ticket_id=ticket_id,
    )


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: uuid.UUID,
    payload: UpdateTicketRequest,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Update ticket.
    """

    return service.update_ticket(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
)
def change_status(
    ticket_id: uuid.UUID,
    payload: UpdateTicketStatusRequest,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Update ticket status.
    """

    return service.change_status(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )


@router.patch(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket(
    ticket_id: uuid.UUID,
    payload: AssignTicketRequest,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Assign ticket.
    """

    return service.assign_ticket(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )


@router.delete(
    "/{ticket_id}",
    response_model=MessageResponse,
)
def delete_ticket(
    ticket_id: uuid.UUID,
    db: DatabaseDependency,
    service: TicketServiceDependency,
):
    """
    Delete ticket.
    """

    service.delete_ticket(
        db=db,
        ticket_id=ticket_id,
    )

    return MessageResponse(
        message="Ticket deleted successfully.",
    )
    
# ==========================================================
# Comment Endpoints
# ==========================================================


@router.post(
    "/{ticket_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    ticket_id: uuid.UUID,
    payload: CreateCommentRequest,
    db: DatabaseDependency,
    service: CommentServiceDependency,
):
    """
    Create a comment for a ticket.
    """

    # TODO:
    # Replace with authenticated user ID
    author_id = uuid.uuid4()

    return service.create_comment(
        db=db,
        ticket_id=ticket_id,
        author_id=author_id,
        payload=payload,
    )


@router.get(
    "/{ticket_id}/comments",
    response_model=list[CommentResponse],
)
def list_comments(
    ticket_id: uuid.UUID,
    db: DatabaseDependency,
    service: CommentServiceDependency,
):
    """
    List all comments for a ticket.
    """

    return service.list_comments(
        db=db,
        ticket_id=ticket_id,
    )


@router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def get_comment(
    comment_id: uuid.UUID,
    db: DatabaseDependency,
    service: CommentServiceDependency,
):
    """
    Get a single comment by ID.
    """

    return service.get_comment(
        db=db,
        comment_id=comment_id,
    )


@router.patch(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def update_comment(
    comment_id: uuid.UUID,
    payload: UpdateCommentRequest,
    db: DatabaseDependency,
    service: CommentServiceDependency,
):
    """
    Update an existing comment.
    """

    return service.update_comment(
        db=db,
        comment_id=comment_id,
        payload=payload,
    )


@router.delete(
    "/comments/{comment_id}",
    response_model=MessageResponse,
)
def delete_comment(
    comment_id: uuid.UUID,
    db: DatabaseDependency,
    service: CommentServiceDependency,
):
    """
    Delete a comment.
    """

    service.delete_comment(
        db=db,
        comment_id=comment_id,
    )

    return MessageResponse(
        message="Comment deleted successfully.",
    )
    
    
    