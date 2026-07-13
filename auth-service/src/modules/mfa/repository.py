from uuid import UUID
from sqlalchemy.orm import Session
from src.modules.user.models import User

class MFARepository:
    def get_user_by_id(self, db: Session, user_id: UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def update_mfa_secret(self, db: Session, user_id: UUID, secret: str | None) -> None:
        user = self.get_user_by_id(db, user_id)
        if user:
            user.mfa_secret = secret
            db.flush()

    def enable_mfa(self, db: Session, user_id: UUID) -> None:
        user = self.get_user_by_id(db, user_id)
        if user:
            user.is_mfa_enabled = True
            db.flush()

    def disable_mfa(self, db: Session, user_id: UUID) -> None:
        user = self.get_user_by_id(db, user_id)
        if user:
            user.is_mfa_enabled = False
            user.mfa_secret = None
            db.flush()
