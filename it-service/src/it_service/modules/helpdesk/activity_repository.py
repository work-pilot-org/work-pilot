from sqlalchemy.orm import Session

from it_service.modules.helpdesk.models import TicketActivity


class TicketActivityRepository:
    """
    Handles database operations for ticket activities.
    """

    def create(
        self,
        db: Session,
        activity: TicketActivity,
    ) -> TicketActivity:

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    def list_by_ticket(
        self,
        db: Session,
        ticket_id,
    ) -> list[TicketActivity]:

        return (
            db.query(TicketActivity)
            .filter(
                TicketActivity.ticket_id == ticket_id
            )
            .order_by(
                TicketActivity.created_at.desc()
            )
            .all()
        )