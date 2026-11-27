from uuid import UUID
from sqlalchemy.orm import Session
from typing import List

from src.modules.invitation.models import Invitation, InvitationStatus


class InvitationRepository:

    def create_invitation(
        self,
        db: Session,
        invitation: Invitation
    ) -> Invitation:
        db.add(invitation)
        db.flush()
        db.refresh(invitation)
        return invitation

    def get_by_id(
        self,
        db: Session,
        invitation_id: UUID
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(Invitation.id == invitation_id)
            .first()
        )

    def get_by_token_hash(
        self,
        db: Session,
        token_hash: str
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(Invitation.token_hash == token_hash)
            .first()
        )

    def get_by_token_hash_for_update(
        self,
        db: Session,
        token_hash: str
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(Invitation.token_hash == token_hash)
            .with_for_update()
            .first()
        )

    def get_by_tenant_and_email(
        self,
        db: Session,
        tenant_id: int,
        email: str
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(
                Invitation.tenant_id == tenant_id,
                Invitation.email == email,
                Invitation.status.in_([InvitationStatus.PENDING])
            )
            .first()
        )

    def get_pending_by_tenant(
        self,
        db: Session,
        tenant_id: int
    ) -> List[Invitation]:
        return (
            db.query(Invitation)
            .filter(
                Invitation.tenant_id == tenant_id,
                Invitation.status == InvitationStatus.PENDING
            )
            .all()
        )

    def get_all_by_tenant(
        self,
        db: Session,
        tenant_id: int
    ) -> List[Invitation]:
        return (
            db.query(Invitation)
            .filter(
                Invitation.tenant_id == tenant_id
            )
            .order_by(Invitation.created_at.desc())
            .all()
        )

    def update_invitation(
        self,
        db: Session,
        invitation: Invitation
    ) -> Invitation:
        db.flush()
        db.refresh(invitation)
        return invitation
