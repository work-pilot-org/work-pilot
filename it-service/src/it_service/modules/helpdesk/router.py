import uuid
from typing import Annotated

from shared_infrastructure.core.security import get_current_user
from fastapi import APIRouter, Depends, Query, Request, status, BackgroundTasks
from sqlalchemy.orm import Session

from shared_infrastructure.core.dependencies import (
    get_current_user_and_set_schema,
    require_permissions,
    verify_ticket_ownership,
)
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
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
from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.publisher import publish_event

router = APIRouter(
    prefix="/tickets",
    tags=["Help Desk"],
    dependencies=[
        Depends(get_current_user),
        Depends(get_current_user_and_set_schema)
    ],
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
    background_tasks: BackgroundTasks,
    db: DatabaseDependency,
    service: TicketServiceDependency,
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Create ticket.
    """
    requester_id = uuid.UUID(current_user.get("sub"))

    result = service.create_ticket(
        db=db,
        requester_id=requester_id,
        payload=payload,
    )
    
    event = EventEnvelope[dict](
        event_type="ticket.created",
        source="it-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "ticket_id": str(result.id),
            "requester_id": str(result.requester_id),
            "assigned_to": str(result.assigned_to) if result.assigned_to else None,
            "category": result.category.value if hasattr(result.category, 'value') else result.category,
            "priority": result.priority.value if hasattr(result.priority, 'value') else result.priority,
            "status": result.status.value if hasattr(result.status, 'value') else result.status,
            "created_at": result.created_at.isoformat()
        }
    )
    background_tasks.add_task(publish_event, "it.ticket", event)
    
    return result


@router.get(
    "",
    response_model=list[TicketResponse],
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
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
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Get ticket.
    """
    verify_ticket_ownership(ticket_id, current_user, db, bypass_permissions=[Permission.TICKETS_MANAGE])

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
    background_tasks: BackgroundTasks,
    db: DatabaseDependency,
    service: TicketServiceDependency,
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Update ticket.
    """
    verify_ticket_ownership(ticket_id, current_user, db, bypass_permissions=[Permission.TICKETS_MANAGE])

    result = service.update_ticket(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )
    
    event = EventEnvelope[dict](
        event_type="ticket.updated",
        source="it-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "ticket_id": str(result.id),
            "requester_id": str(result.requester_id),
            "assigned_to": str(result.assigned_to) if result.assigned_to else None,
            "category": result.category.value if hasattr(result.category, 'value') else result.category,
            "priority": result.priority.value if hasattr(result.priority, 'value') else result.priority,
            "status": result.status.value if hasattr(result.status, 'value') else result.status,
            "created_at": result.created_at.isoformat()
        }
    )
    background_tasks.add_task(publish_event, "it.ticket", event)
    
    return result


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
)
def change_status(
    ticket_id: uuid.UUID,
    payload: UpdateTicketStatusRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseDependency,
    service: TicketServiceDependency,
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Update ticket status.
    """

    result = service.change_status(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )
    
    event = EventEnvelope[dict](
        event_type="ticket.status_changed",
        source="it-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "ticket_id": str(result.id),
            "requester_id": str(result.requester_id),
            "assigned_to": str(result.assigned_to) if result.assigned_to else None,
            "category": result.category.value if hasattr(result.category, 'value') else result.category,
            "priority": result.priority.value if hasattr(result.priority, 'value') else result.priority,
            "status": result.status.value if hasattr(result.status, 'value') else result.status,
            "created_at": result.created_at.isoformat()
        }
    )
    background_tasks.add_task(publish_event, "it.ticket", event)
    
    return result


@router.patch(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
)
def assign_ticket(
    ticket_id: uuid.UUID,
    payload: AssignTicketRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseDependency,
    service: TicketServiceDependency,
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Assign ticket.
    """

    result = service.assign_ticket(
        db=db,
        ticket_id=ticket_id,
        payload=payload,
    )
    
    event = EventEnvelope[dict](
        event_type="ticket.assigned",
        source="it-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "ticket_id": str(result.id),
            "requester_id": str(result.requester_id),
            "assigned_to": str(result.assigned_to) if result.assigned_to else None,
            "category": result.category.value if hasattr(result.category, 'value') else result.category,
            "priority": result.priority.value if hasattr(result.priority, 'value') else result.priority,
            "status": result.status.value if hasattr(result.status, 'value') else result.status,
            "created_at": result.created_at.isoformat()
        }
    )
    background_tasks.add_task(publish_event, "it.ticket", event)
    
    return result


@router.delete(
    "/{ticket_id}",
    response_model=MessageResponse,
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
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
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Create a comment for a ticket.
    """
    verify_ticket_ownership(ticket_id, current_user, db, bypass_permissions=[Permission.TICKETS_MANAGE])
    
    author_id = uuid.UUID(current_user.get("sub"))

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
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    List all comments for a ticket.
    """
    verify_ticket_ownership(ticket_id, current_user, db, bypass_permissions=[Permission.TICKETS_MANAGE])

    return service.list_comments(
        db=db,
        ticket_id=ticket_id,
    )


@router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
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
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
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
    dependencies=[Depends(require_permissions([Permission.TICKETS_MANAGE]))],
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