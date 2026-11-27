import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
import structlog

from shared_infrastructure.core.config import settings
from notification_service.core.exceptions import (
    EmailConfigurationError,
    EmailDeliveryError,
)

logger = structlog.get_logger(__name__)


class EmailService:
    """
    Service responsible for compiling and delivering emails using SMTP.
    """

    def __init__(self) -> None:
        template_path = Path(__file__).parent.parent / "templates"
        self.environment = Environment(
            loader=FileSystemLoader(template_path)
        )

        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from = settings.SMTP_FROM
        
        self.email_from_name = settings.EMAIL_FROM_NAME

        # Defensive validation of required environment configuration
        if not self.smtp_host or not self.smtp_port:
            raise EmailConfigurationError("SMTP_HOST and SMTP_PORT are not configured.")
        if not self.smtp_from:
            raise EmailConfigurationError("SMTP_FROM is not configured.")

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text_content: str | None = None,
    ) -> int:
        """
        Sends a generic email using SMTP.

        Returns:
            int: The HTTP status code returned (200 for success).
        """
        from_email = f"{self.email_from_name} <{self.smtp_from}>" if self.email_from_name else self.smtp_from

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        
        if plain_text_content:
            msg.set_content(plain_text_content)
            msg.add_alternative(html_content, subtype="html")
        else:
            msg.set_content(html_content, subtype="html")

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(
                "Email sent successfully",
                to_email=to_email,
            )
            return 200

        except smtplib.SMTPException as e:
            logger.error(
                "SMTP email delivery failed",
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
            int: The HTTP status code returned (200 on success).
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
