import pytest
from unittest.mock import MagicMock, patch

from shared_infrastructure.core.config import settings

from notification_service.core.email import EmailService
from notification_service.core.exceptions import (
    EmailConfigurationError,
    EmailDeliveryError,
)


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setattr(
        settings,
        "SENDGRID_API_KEY",
        "SG.test_key",
    )
    monkeypatch.setattr(
        settings,
        "EMAIL_FROM",
        "test@workpilot.com",
    )
    monkeypatch.setattr(
        settings,
        "EMAIL_FROM_NAME",
        "WorkPilot Test",
    )


def test_email_service_imports_and_instantiates(mock_settings):
    service = EmailService()

    assert service.api_key == "SG.test_key"
    assert service.email_from == "test@workpilot.com"
    assert service.email_from_name == "WorkPilot Test"


def test_email_service_fails_on_missing_config(monkeypatch):
    monkeypatch.setattr(
        settings,
        "SENDGRID_API_KEY",
        None,
    )

    with pytest.raises(
        EmailConfigurationError,
        match="SENDGRID_API_KEY is not configured",
    ):
        EmailService()

    monkeypatch.setattr(
        settings,
        "SENDGRID_API_KEY",
        "SG.key",
    )
    monkeypatch.setattr(
        settings,
        "EMAIL_FROM",
        "",
    )

    with pytest.raises(
        EmailConfigurationError,
        match="EMAIL_FROM is not configured",
    ):
        EmailService()


@patch("notification_service.core.email.SendGridAPIClient")
def test_send_generic_email_success(
    mock_client_class,
    mock_settings,
):
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.status_code = 202

    mock_client.send.return_value = mock_response
    mock_client_class.return_value = mock_client

    service = EmailService()

    status = service.send_email(
        to_email="recipient@example.com",
        subject="Test Subject",
        html_content="<p>Test</p>",
        plain_text_content="Test plain text",
    )

    assert status == 202

    mock_client_class.assert_called_once_with(
        "SG.test_key"
    )

    mock_client.send.assert_called_once()

    # Verify SendGrid Mail payload.
    mail_call_arg = mock_client.send.call_args[0][0]

    assert mail_call_arg.from_email.email == "test@workpilot.com"
    assert mail_call_arg.from_email.name == "WorkPilot Test"
    assert mail_call_arg.subject.subject == "Test Subject"


@patch("notification_service.core.email.SendGridAPIClient")
def test_send_generic_email_delivery_failure(
    mock_client_class,
    mock_settings,
):
    mock_client = MagicMock()

    mock_client.send.side_effect = Exception(
        "SendGrid connection timed out"
    )

    mock_client_class.return_value = mock_client

    service = EmailService()

    with pytest.raises(
        EmailDeliveryError,
        match="Failed to deliver email",
    ):
        service.send_email(
            to_email="recipient@example.com",
            subject="Test Subject",
            html_content="<p>Test</p>",
        )


def test_send_template_email_renders_jinja(
    mock_settings,
):
    service = EmailService()

    # Mock only the service's send_email method.
    # This test is specifically testing Jinja rendering
    # and delegation to send_email().
    with patch.object(
        service,
        "send_email",
        return_value=202,
    ) as mock_send:
        status = service.send_template_email(
            to_email="recipient@example.com",
            subject="Password Reset",
            template_name="password_reset.html",
            context={
                "reset_link": (
                    "https://workpilot.com/reset?token=123"
                )
            },
        )

    assert status == 202

    mock_send.assert_called_once()

    call_kwargs = mock_send.call_args.kwargs

    assert (
        call_kwargs["to_email"]
        == "recipient@example.com"
    )

    assert (
        call_kwargs["subject"]
        == "Password Reset"
    )

    assert (
        "https://workpilot.com/reset?token=123"
        in call_kwargs["html_content"]
    )