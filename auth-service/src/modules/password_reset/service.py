from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.email.email_service import EmailService
from src.core.security import (
    generate_reset_token,
    hash_password,
    hash_reset_token,
)
from src.modules.password_reset.models import PasswordResetToken
from src.modules.password_reset.repository import PasswordResetRepository
from src.modules.user.repository import UserRepository


class PasswordResetService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.password_reset_repository = PasswordResetRepository()
        self.email_service = EmailService()

    def forgot_password(
        self,
        db: Session,
        email: str,
    ):
        """
        Generate password reset token
        and send reset email.
        """

        user = self.user_repository.get_user_by_email(
            db=db,
            email=email,
        )

        # Don't reveal whether the email exists
        if user is None:
            return

        # Generate secure token
        reset_token = generate_reset_token()

        # Hash token before storing
        token_hash = hash_reset_token(reset_token)

        # Save token
        password_reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow()
            + timedelta(
                minutes=settings.RESET_TOKEN_EXPIRE_MINUTES
            ),
            used=False,
        )

        self.password_reset_repository.create_token(
            db=db,
            token=password_reset_token,
        )

        db.commit()

        # Build reset link
        reset_link = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password?token={reset_token}"
        )

        # Send email
        self.email_service.send_password_reset_email(
            email=user.email,
            reset_link=reset_link,
        )

    def reset_password(
        self,
        db: Session,
        token: str,
        new_password: str,
    ):
        """
        Validate token.
        Update password.
        Mark token as used.
        """

        # Hash incoming token
        token_hash = hash_reset_token(token)

        # Find stored token
        password_reset_token = (
            self.password_reset_repository.get_by_token_hash(
                db=db,
                token_hash=token_hash,
            )
        )

        # Validate token exists
        if password_reset_token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token.",
            )

        # Validate token is not expired
        if password_reset_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired.",
            )

        # Validate token has not been used
        if password_reset_token.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has already been used.",
            )

        # Fetch user
        user = self.user_repository.get_user_by_id(
            db=db,
            user_id=password_reset_token.user_id,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # Hash new password
        user.password = hash_password(new_password)

        # Update user
        self.user_repository.update_user(
            db=db,
            user=user,
        )

        # Mark token as used
        password_reset_token.used = True

        self.password_reset_repository.update(
            db=db,
            token=password_reset_token,
        )

        db.commit()