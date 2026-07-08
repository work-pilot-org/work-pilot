from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.password_reset.models import PasswordResetToken


class PasswordResetRepository:

    def create_token(
        self,
        db: Session,
        token: PasswordResetToken,
    ) -> PasswordResetToken:

        db.add(token)
        db.flush()
        db.refresh(token)

        return token

    def get_by_token_hash(
        self,
        db: Session,
        token_hash: str,
    ) -> PasswordResetToken | None:

        return (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.token_hash == token_hash
            )
            .first()
        )

    def get_active_token_for_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> PasswordResetToken | None:

        return (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used.is_(False),
                PasswordResetToken.expires_at > datetime.utcnow(),
            )
            .first()
        )

    def update(
        self,
        db: Session,
        token: PasswordResetToken,
    ) -> PasswordResetToken:

        db.flush()
        db.refresh(token)

        return token