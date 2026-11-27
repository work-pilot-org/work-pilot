import sys
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from shared_infrastructure.database.session import SessionLocal
from src.modules.invitation.models import Invitation, InvitationStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_cleanup():
    logger.info("Starting invitation cleanup job...")
    db: Session = SessionLocal()
    try:
        # Mark pending invitations that have passed their expires_at date as EXPIRED
        now = datetime.utcnow()
        expired_invitations = db.query(Invitation).filter(
            Invitation.status == InvitationStatus.PENDING,
            Invitation.expires_at < now
        ).all()

        for inv in expired_invitations:
            inv.status = InvitationStatus.EXPIRED
            logger.info(f"Marked invitation {inv.id} for {inv.email} as EXPIRED.")
        
        # Hard delete revoked or expired invitations older than 30 days
        thirty_days_ago = now - timedelta(days=30)
        old_invitations = db.query(Invitation).filter(
            Invitation.status.in_([InvitationStatus.EXPIRED, InvitationStatus.REVOKED]),
            Invitation.updated_at < thirty_days_ago
        ).all()
        
        for inv in old_invitations:
            db.delete(inv)
            logger.info(f"Deleted old invitation {inv.id} for {inv.email}.")

        db.commit()
        logger.info(f"Cleanup completed. Expired: {len(expired_invitations)}, Deleted: {len(old_invitations)}.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during cleanup: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    run_cleanup()
