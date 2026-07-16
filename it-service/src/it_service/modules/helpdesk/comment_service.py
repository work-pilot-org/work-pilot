import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.helpdesk.activity_actions import ActivityAction
from it_service.modules.helpdesk.activity_service import ActivityService
from it_service.modules.helpdesk.comment_repository import CommentRepository
from it_service.modules.helpdesk.models.ticket_comment import TicketComment
from it_service.modules.helpdesk.schemas import (
    CreateCommentRequest,
    UpdateCommentRequest,
)


class CommentService:
    """
    Handles all business logic related to ticket comments.
    """

    def __init__(
        self,
        repository: CommentRepository,
        activity_service: ActivityService,
    ):
        self.repository = repository
        self.activity_service = activity_service

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _get_comment(
        self,
        db: Session,
        comment_id: uuid.UUID,
    ) -> TicketComment:

        comment = self.repository.get_by_id(
            db,
            comment_id,
        )

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found.",
            )

        return comment

    # ==========================================================
    # CRUD
    # ==========================================================

    def create_comment(
        self,
        db: Session,
        ticket_id: uuid.UUID,
        author_id: uuid.UUID,
        payload: CreateCommentRequest,
    ) -> TicketComment:

        comment = TicketComment(
            ticket_id=ticket_id,
            author_id=author_id,
            comment=payload.comment,
            comment_type=payload.comment_type,
        )

        saved_comment = self.repository.create(
            db,
            comment,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=ticket_id,
            performed_by=author_id,
            action=ActivityAction.COMMENT_ADDED,
            new_value={
                "comment_id": str(saved_comment.id),
            },
        )

        return saved_comment

    def get_comment(
        self,
        db: Session,
        comment_id: uuid.UUID,
    ) -> TicketComment:

        return self._get_comment(
            db,
            comment_id,
        )

    def list_comments(
        self,
        db: Session,
        ticket_id: uuid.UUID,
    ) -> list[TicketComment]:

        return self.repository.get_by_ticket(
            db,
            ticket_id,
        )

    def update_comment(
        self,
        db: Session,
        comment_id: uuid.UUID,
        payload: UpdateCommentRequest,
    ) -> TicketComment:

        comment = self._get_comment(
            db,
            comment_id,
        )

        old_comment = comment.comment

        comment.comment = payload.comment
        comment.is_edited = True
        comment.updated_at = datetime.utcnow()

        updated_comment = self.repository.update(
            db,
            comment,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=comment.ticket_id,
            performed_by=comment.author_id,
            action=ActivityAction.COMMENT_UPDATED,
            old_value={
                "comment": old_comment,
            },
            new_value={
                "comment": payload.comment,
            },
        )

        return updated_comment

    def delete_comment(
        self,
        db: Session,
        comment_id: uuid.UUID,
    ) -> None:

        comment = self._get_comment(
            db,
            comment_id,
        )

        self.activity_service.log_activity(
            db=db,
            ticket_id=comment.ticket_id,
            performed_by=comment.author_id,
            action=ActivityAction.COMMENT_DELETED,
        )

        self.repository.delete(
            db,
            comment,
        )