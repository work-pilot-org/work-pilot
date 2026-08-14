from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import structlog

from shared_infrastructure.core.config import settings
from notification_service.core.exceptions import (
    EmailConfigurationError,
    EmailDeliveryError,
)

logger = structlog.get_logger(__name__)


class EmailService:
    """
    Service responsible for compiling and delivering emails using SendGrid.
    """

    def __init__(self) -> None:
        template_path = Path(__file__).parent.parent / "templates"
        self.environment = Environment(
            loader=FileSystemLoader(template_path)
        )

        self.api_key = settings.SENDGRID_API_KEY
        self.email_from = settings.EMAIL_FROM
        self.email_from_name = settings.EMAIL_FROM_NAME

        # Defensive validation of required environment configuration
        if not self.api_key:
            raise EmailConfigurationError("SENDGRID_API_KEY is not configured.")
        if not self.email_from:
            raise EmailConfigurationError("EMAIL_FROM is not configured.")

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text_content: str | None = None,
    ) -> int:
        """
        Sends a generic email using SendGrid.

        Returns:
            int: The HTTP status code returned by SendGrid.
        """
        message = Mail(
            from_email=self.email_from,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=plain_text_content,
        )

        if self.email_from_name:
            message.from_email.name = self.email_from_name

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            logger.info(
                "Email sent successfully",
                to_email=to_email,
                status_code=response.status_code,
            )
            return response.status_code

        except Exception as e:
            logger.error(
                "SendGrid email delivery failed",
                to_email=to_email,
                error=str(e),
            )
            raise EmailDeliveryError(f"Failed to deliver email to {to_email} due to provider error.") from e

    def send_template_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: dict[str, Any],
    ) -> int:
        """
        Loads a Jinja2 template, renders it with context, and sends it.

        Returns:
            int: The HTTP status code returned by SendGrid.
        """
        try:
            template = self.environment.get_template(template_name)
            html_content = template.render(**context)
        except Exception as e:
            logger.error(
                "Failed to render Jinja2 email template",
                template_name=template_name,
                error=str(e),
            )
            raise EmailDeliveryError(f"Failed to render template: {template_name}") from e

        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
        )
