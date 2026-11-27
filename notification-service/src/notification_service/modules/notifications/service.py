from datetime import datetime, timezone

from sqlalchemy.orm import Session

from notification_service.core.email import EmailService
from notification_service.core.exceptions import NotificationEmailError
from notification_service.modules.notifications.enums import (
    Channel,
    NotificationStatus,
    NotificationType,
)
from notification_service.modules.notifications.models import NotificationLog
from notification_service.modules.notifications.schemas import (
    NotificationCreate,
    NotificationResponse,
)


class NotificationService:
    """
    Business service responsible for creating notification logs
    and delivering notifications through the appropriate channel.
    """

    def __init__(
        self,
        email_service: EmailService | None = None,
    ) -> None:
        self.email_service = email_service or EmailService()

    def send_notification(
        self,
        db: Session,
        notification: NotificationCreate,
        tenant_id: str,
    ) -> NotificationResponse:
        """
        Create a notification log, deliver the notification,
        and update the delivery status.

        tenant_id is supplied by the trusted authentication context.
        It must never come from the client request body.
        """

        if not tenant_id or not tenant_id.strip():
            raise ValueError("Tenant ID is required.")

        tenant_id = tenant_id.strip()

        notification_log = NotificationLog(
            recipient_id=notification.recipient_id,
            tenant_id=tenant_id,
            channel=notification.channel,
            notification_type=notification.notification_type,
            subject=notification.subject,
            body=notification.body,
            status=NotificationStatus.PENDING,
        )

        db.add(notification_log)
        db.commit()
        db.refresh(notification_log)

        try:
            self._deliver(
                notification=notification,
            )

            notification_log.status = NotificationStatus.SENT
            notification_log.sent_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(notification_log)

        except NotificationEmailError as exc:
            notification_log.status = NotificationStatus.FAILED
            notification_log.error_message = str(exc)

            db.commit()
            db.refresh(notification_log)

        except Exception as exc:
            notification_log.status = NotificationStatus.FAILED
            notification_log.error_message = str(exc)

            db.commit()
            db.refresh(notification_log)

        return self._to_response(notification_log)

    def _deliver(
        self,
        notification: NotificationCreate,
    ) -> None:
        """
        Deliver the notification according to its channel.
        """

        if notification.channel == Channel.EMAIL:
            self.email_service.send_email(
                to_email=str(notification.recipient_email),
                subject=notification.subject,
                html_content=notification.body,
            )
            return

        raise ValueError(
            f"Unsupported notification channel: {notification.channel}"
        )

    @staticmethod
    def _to_response(
        notification: NotificationLog,
    ) -> NotificationResponse:
        """
        Convert the database model into the API response schema.
        """

        return NotificationResponse(
            id=notification.id,
            recipient_id=notification.recipient_id,
            channel=notification.channel,
            notification_type=notification.notification_type,
            subject=notification.subject,
            status=notification.status.value,
            created_at=notification.created_at.isoformat(),
            sent_at=(
                notification.sent_at.isoformat()
                if notification.sent_at
                else None
            ),
        )