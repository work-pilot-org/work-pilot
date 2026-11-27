from datetime import datetime, timezone
from unittest.mock import MagicMock

from notification_service.modules.notifications.enums import (
    Channel,
    NotificationStatus,
    NotificationType,
)
from notification_service.modules.notifications.schemas import NotificationCreate
from notification_service.modules.notifications.service import NotificationService


def create_notification() -> NotificationCreate:
    return NotificationCreate(
        recipient_id="user-123",
        recipient_email="recipient@example.com",
        channel=Channel.EMAIL,
        notification_type=NotificationType.WORKFLOW_APPROVAL,
        subject="Approval Required",
        body="<p>Please approve this request.</p>",
    )


def create_mock_db() -> MagicMock:
    db = MagicMock()

    def refresh_model(model):
        if model.id is None:
            model.id = "notification-123"

        if model.created_at is None:
            model.created_at = datetime.now(timezone.utc)

    db.refresh.side_effect = refresh_model

    return db


def test_send_notification_success():
    db = create_mock_db()

    email_service = MagicMock()
    email_service.send_email.return_value = 202

    service = NotificationService(
        email_service=email_service,
    )

    notification = create_notification()

    result = service.send_notification(
        db=db,
        notification=notification,
        tenant_id="tenant-123",
    )

    assert result.id == "notification-123"
    assert result.recipient_id == "user-123"
    assert result.channel == Channel.EMAIL
    assert result.notification_type == NotificationType.WORKFLOW_APPROVAL
    assert result.subject == "Approval Required"
    assert result.status == NotificationStatus.SENT.value
    assert result.created_at is not None
    assert result.sent_at is not None

    email_service.send_email.assert_called_once_with(
        to_email="recipient@example.com",
        subject="Approval Required",
        html_content="<p>Please approve this request.</p>",
    )

    db.add.assert_called_once()
    db.commit.assert_called()
    db.refresh.assert_called()


def test_send_notification_failure_marks_notification_failed():
    db = create_mock_db()

    email_service = MagicMock()
    email_service.send_email.side_effect = Exception(
        "SendGrid connection failed"
    )

    service = NotificationService(
        email_service=email_service,
    )

    notification = create_notification()

    result = service.send_notification(
        db=db,
        notification=notification,
        tenant_id="tenant-123",
    )

    assert result.id == "notification-123"
    assert result.status == NotificationStatus.FAILED.value
    assert result.created_at is not None
    assert result.sent_at is None

    email_service.send_email.assert_called_once()


def test_send_notification_requires_tenant_id():
    db = create_mock_db()

    email_service = MagicMock()

    service = NotificationService(
        email_service=email_service,
    )

    notification = create_notification()

    try:
        service.send_notification(
            db=db,
            notification=notification,
            tenant_id="",
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Tenant ID is required."

    email_service.send_email.assert_not_called()
    db.add.assert_not_called()


def test_notification_tenant_id_comes_from_service_argument():
    db = create_mock_db()

    email_service = MagicMock()
    email_service.send_email.return_value = 202

    service = NotificationService(
        email_service=email_service,
    )

    notification = create_notification()

    service.send_notification(
        db=db,
        notification=notification,
        tenant_id="tenant-from-auth",
    )

    notification_log = db.add.call_args[0][0]

    assert notification_log.tenant_id == "tenant-from-auth"

    # The tenant must come from the trusted service/auth context,
    # not from the notification request payload.
    assert notification_log.tenant_id != notification.recipient_id


def test_unsupported_channel_raises_error():
    db = create_mock_db()

    email_service = MagicMock()

    service = NotificationService(
        email_service=email_service,
    )

    notification = create_notification()

    # Bypass Pydantic validation intentionally so we can
    # test the service's defensive channel handling.
    object.__setattr__(notification, "channel", "sms")

    try:
        service._deliver(notification)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported notification channel" in str(exc)

    email_service.send_email.assert_not_called()