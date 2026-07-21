import uuid

from sqlalchemy.orm import Session

from it_service.modules.helpdesk.activity_actions import ActivityAction
from it_service.modules.helpdesk.activity_repository import TicketActivityRepository
from it_service.modules.helpdesk.models.ticket_activity import TicketActivity


class ActivityService:
    """
    Handles audit logging for ticket activities.
    """

    def __init__(self, repository: TicketActivityRepository):
        self.repository = repository

    def log_activity(
        self,
        db: Session,
        ticket_id: uuid.UUID,
        action: ActivityAction | str,
        performed_by: uuid.UUID,
        old_value: dict | None = None,
        new_value: dict | None = None,
    ) -> TicketActivity:
        activity = TicketActivity(
            ticket_id=ticket_id,
            action=action.value if isinstance(action, ActivityAction) else action,
            performed_by=performed_by,
            old_value=old_value,
            new_value=new_value,
        )
        return self.repository.create(db, activity)

    def list_activities(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> list[TicketActivity]:
        return self.repository.list_by_ticket(db, ticket_id)
