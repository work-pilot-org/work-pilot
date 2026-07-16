from uuid import UUID

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session

from it_service.modules.helpdesk.enums import (
    TicketPriority,
    TicketStatus,
)
from it_service.modules.helpdesk.models import Ticket


class TicketRepository:
    """
    Repository responsible for database operations only.

    No business logic should exist here.
    """

    def create(
        self,
        db: Session,
        ticket: Ticket,
    ) -> Ticket:

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket

    def get_by_id(
        self,
        db: Session,
        ticket_id: UUID,
    ) -> Ticket | None:

        statement = (
            select(Ticket)
            .where(Ticket.id == ticket_id)
        )

        return db.scalar(statement)

    def get_by_ticket_number(
        self,
        db: Session,
        ticket_number: str,
    ) -> Ticket | None:

        statement = (
            select(Ticket)
            .where(Ticket.ticket_number == ticket_number)
        )

        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        assigned_to: UUID | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
        descending: bool = True,
    ) -> list[Ticket]:

        statement = select(Ticket)

        if status:
            statement = statement.where(
                Ticket.status == status
            )

        if priority:
            statement = statement.where(
                Ticket.priority == priority
            )

        if assigned_to:
            statement = statement.where(
                Ticket.assigned_to == assigned_to
            )

        if search:
            statement = statement.where(
                or_(
                    Ticket.title.ilike(f"%{search}%"),
                    Ticket.description.ilike(f"%{search}%"),
                    Ticket.ticket_number.ilike(f"%{search}%"),
                )
            )

        if descending:
            statement = statement.order_by(
                desc(Ticket.created_at)
            )
        else:
            statement = statement.order_by(
                asc(Ticket.created_at)
            )

        statement = statement.offset(skip).limit(limit)

        return list(db.scalars(statement).all())

    def count(
        self,
        db: Session,
    ) -> int:

        return len(
            db.scalars(
                select(Ticket)
            ).all()
        )

    def exists(
        self,
        db: Session,
        ticket_id: UUID,
    ) -> bool:

        return self.get_by_id(
            db,
            ticket_id,
        ) is not None

    def save(
        self,
        db: Session,
        ticket: Ticket,
    ) -> Ticket:

        db.commit()
        db.refresh(ticket)

        return ticket

    def delete(
        self,
        db: Session,
        ticket: Ticket,
    ) -> None:

        db.delete(ticket)
        db.commit()