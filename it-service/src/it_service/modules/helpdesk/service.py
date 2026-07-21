import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.helpdesk.activity_actions import ActivityAction
from it_service.modules.helpdesk.activity_service import ActivityService
from it_service.modules.helpdesk.enums import TicketStatus
from it_service.modules.helpdesk.models import Ticket
from it_service.modules.helpdesk.repository import TicketRepository
from it_service.modules.helpdesk.schemas import (
    AssignTicketRequest,
    CreateTicketRequest,
    UpdateTicketRequest,
    UpdateTicketStatusRequest,
)


class TicketService:

    def __init__(
        self,
        repository: TicketRepository,
        activity_service: ActivityService,
    ):
        self.repository = repository
        self.activity_service = activity_service

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _generate_ticket_number(self) -> str:
        """
        Temporary ticket number.

        TODO:
        Replace with sequential numbering.

        Example:
            IT-2026-000001
        """

        year = datetime.utcnow().year
        unique = uuid.uuid4().hex[:6].upper()

        return f"IT-{year}-{unique}"

    def _get_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> Ticket:

        ticket = self.repository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        return ticket

    def _validate_status_transition(
        self,
        current: TicketStatus,
        new: TicketStatus,
    ) -> None:
        """
        Validate ticket status transitions.
        """

        allowed = {
            TicketStatus.OPEN: {
                TicketStatus.IN_PROGRESS,
                TicketStatus.CANCELLED,
            },
            TicketStatus.IN_PROGRESS: {
                TicketStatus.RESOLVED,
                TicketStatus.ON_HOLD,
                TicketStatus.CANCELLED,
            },
            TicketStatus.ON_HOLD: {
                TicketStatus.IN_PROGRESS,
                TicketStatus.CANCELLED,
            },
            TicketStatus.RESOLVED: {
                TicketStatus.CLOSED,
            },
            TicketStatus.CLOSED: set(),
            TicketStatus.CANCELLED: set(),
        }

        if new not in allowed[current]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot change ticket from {current.value} to {new.value}.",
            )

    # ==========================================================
    # CRUD
    # ==========================================================

    def create_ticket(
        self,
        db: Session,
        requester_id: uuid.UUID,
        payload: CreateTicketRequest,
    ) -> Ticket:

        ticket = Ticket(
            ticket_number=self._generate_ticket_number(),
            title=payload.title,
            description=payload.description,
            category=payload.category,
            priority=payload.priority,
            source=payload.source,
            requester_id=requester_id,
            status=TicketStatus.OPEN,
        )

        saved_ticket = self.repository.create(
            db,
            ticket,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=saved_ticket.id,
            action=ActivityAction.TICKET_CREATED,
            performed_by=requester_id,
        )

        return saved_ticket

    def get_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> Ticket:

        return self._get_ticket(
            db,
            ticket_id,
        )

    def list_tickets(
        self,
        db: Session,
        **filters,
    ):

        return self.repository.list(
            db,
            **filters,
        )

    def update_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
        payload: UpdateTicketRequest,
    ) -> Ticket:

        ticket = self._get_ticket(
            db,
            ticket_id,
        )

        updates = payload.model_dump(
            exclude_unset=True,
        )

        old_values = {}

        for field, value in updates.items():
            old_values[field] = getattr(ticket, field)
            setattr(ticket, field, value)

        saved_ticket = self.repository.save(
            db,
            ticket,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=saved_ticket.id,
            action=ActivityAction.TICKET_UPDATED,
            performed_by=saved_ticket.requester_id,
            old_value=old_values,
            new_value=updates,
        )

        return saved_ticket

    def assign_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
        payload: AssignTicketRequest,
    ) -> Ticket:

        ticket = self._get_ticket(
            db,
            ticket_id,
        )

        old_assignee = ticket.assigned_to

        ticket.assigned_to = payload.assigned_to

        saved_ticket = self.repository.save(
            db,
            ticket,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=saved_ticket.id,
            action=ActivityAction.ASSIGNED,
            performed_by=payload.assigned_to,
            old_value={
                "assigned_to": str(old_assignee)
                if old_assignee
                else None
            },
            new_value={
                "assigned_to": str(payload.assigned_to)
            },
        )

        return saved_ticket

    def change_status(
        self,
        db: Session,
        ticket_id: uuid.UUID,
        payload: UpdateTicketStatusRequest,
    ) -> Ticket:

        ticket = self._get_ticket(
            db,
            ticket_id,
        )

        self._validate_status_transition(
            ticket.status,
            payload.status,
        )

        previous_status = ticket.status

        ticket.status = payload.status

        if payload.resolution:
            ticket.resolution = payload.resolution

        if payload.status == TicketStatus.RESOLVED:
            ticket.resolved_at = datetime.utcnow()

        if payload.status == TicketStatus.CLOSED:
            ticket.closed_at = datetime.utcnow()

        saved_ticket = self.repository.save(
            db,
            ticket,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=saved_ticket.id,
            action=ActivityAction.STATUS_CHANGED,
            performed_by=saved_ticket.requester_id,
            old_value={
                "status": previous_status.value,
            },
            new_value={
                "status": saved_ticket.status.value,
            },
        )

        return saved_ticket

    def delete_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> None:

        ticket = self._get_ticket(
            db,
            ticket_id,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=ticket.id,
            action=ActivityAction.TICKET_DELETED,
            performed_by=ticket.requester_id,
        )

        self.repository.delete(
            db,
            ticket,
        )