import smtplib
from email.message import EmailMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from shared_infrastructure.core.config import settings


class EmailService:
    """
    Service responsible for sending application emails via SMTP.
    """

    def __init__(self) -> None:
        template_path = Path(__file__).parent / "templates"

        self.environment = Environment(
            loader=FileSystemLoader(template_path)
        )

        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from = settings.SMTP_FROM
        
        self.email_from_name = settings.EMAIL_FROM_NAME

    def _send_email_via_smtp(self, msg: EmailMessage) -> None:
        if not self.smtp_host or not self.smtp_port:
            print("SMTP_HOST or SMTP_PORT not configured. Skipping email send.")
            return

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                print(f"Email sent successfully to {msg['To']}")
        except smtplib.SMTPException as e:
            print("========== SMTP ERROR ==========")
            print(f"Failed to send email to {msg['To']}")
            print("================================")
            raise

    def send_password_reset_email(
        self,
        email: str,
        reset_link: str,
    ) -> None:
        """
        Send password reset email using SMTP.
        """

        # Load HTML template
        template = self.environment.get_template(
            "password_reset.html"
        )

        # Render HTML
        html_content = template.render(
            reset_link=reset_link,
        )

        # Create email sender format
        from_email = f"{self.email_from_name} <{self.smtp_from}>" if self.email_from_name else self.smtp_from

        msg = EmailMessage()
        msg["Subject"] = "Reset Your WorkPilot Password"
        msg["From"] = from_email
        msg["To"] = email
        msg.add_alternative(html_content, subtype="html")

        self._send_email_via_smtp(msg)

    def send_invitation_email(
        self,
        email: str,
        invite_link: str,
        company_name: str,
        role: str,
        expiry_date: str,
    ) -> None:
        """
        Send an employee invitation email using SMTP.
        """

        # Load HTML template
        template = self.environment.get_template(
            "invitation.html"
        )

        # Render HTML
        html_content = template.render(
            invite_link=invite_link,
            company_name=company_name,
            role=role,
            expiry_date=expiry_date,
        )

        # Plain text content
        plain_text_content = (
            f"You have been invited to join {company_name} on WorkPilot as a {role}.\n\n"
            f"Please navigate to the following link to accept the invitation. This link will expire on {expiry_date}:\n"
            f"{invite_link}\n\n"
            f"If you did not expect this invitation, you can safely ignore this email."
        )

        # Create email sender format
        from_email = f"{self.email_from_name} <{self.smtp_from}>" if self.email_from_name else self.smtp_from

        msg = EmailMessage()
        msg["Subject"] = f"You've been invited to join {company_name} on WorkPilot"
        msg["From"] = from_email
        msg["To"] = email
        msg.set_content(plain_text_content)
        msg.add_alternative(html_content, subtype="html")

        self._send_email_via_smtp(msg)

