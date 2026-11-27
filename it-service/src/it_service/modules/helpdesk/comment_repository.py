import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from it_service.modules.helpdesk.models.ticket_comment import (
    TicketComment,
)


class CommentRepository:
    """
    Repository responsible for all database
    operations related to ticket comments.
    """

    def create(
        self,
        db: Session,
        comment: TicketComment,
    ) -> TicketComment:
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def get_by_id(
        self,
        db: Session,
        comment_id: uuid.UUID,
    ) -> TicketComment | None:

        statement = (
            select(TicketComment)
            .where(
                TicketComment.id == comment_id
            )
        )

        return db.scalar(statement)

    def get_by_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> list[TicketComment]:

        statement = (
            select(TicketComment)
            .where(
                TicketComment.ticket_id == ticket_id
            )
            .order_by(
                TicketComment.created_at.asc()
            )
        )

        return list(
            db.scalars(statement).all()
        )

    def update(
        self,
        db: Session,
        comment: TicketComment,
    ) -> TicketComment:

        db.commit()
        db.refresh(comment)

        return comment

    def delete(
        self,
        db: Session,
        comment: TicketComment,
    ) -> None:

        db.delete(comment)
        db.commit()

    def exists(
        self,
        db: Session,
        comment_id: uuid.UUID,
    ) -> bool:

        statement = (
            select(TicketComment.id)
            .where(
                TicketComment.id == comment_id
            )
        )

        return db.scalar(statement) is not None

    def count_by_ticket(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> int:

        statement = (
            select(TicketComment)
            .where(
                TicketComment.ticket_id == ticket_id
            )
        )

        return len(
            list(
                db.scalars(statement).all()
            )
        )