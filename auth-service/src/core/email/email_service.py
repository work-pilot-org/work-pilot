from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.core.config import settings


class EmailService:
    """
    Service responsible for sending application emails.
    """

    def __init__(self) -> None:
        template_path = Path(__file__).parent / "templates"

        self.environment = Environment(
            loader=FileSystemLoader(template_path)
        )

    def send_password_reset_email(
        self,
        email: str,
        reset_link: str,
    ) -> None:
        """
        Send password reset email using SendGrid.
        """

        # Load HTML template
        template = self.environment.get_template(
            "password_reset.html"
        )

        # Render HTML
        html_content = template.render(
            reset_link=reset_link,
        )

        # Create email
        message = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=email,
            subject="Reset Your WorkPilot Password",
            html_content=html_content,
        )

        # Set sender display name
        message.from_email.name = settings.EMAIL_FROM_NAME

        try:
            sg = SendGridAPIClient(
                settings.SENDGRID_API_KEY
            )

            response = sg.send(message)

            print(
                f"Password reset email sent successfully "
                f"(Status Code: {response.status_code})"
            )

        except Exception as e:
            print("========== SENDGRID ERROR ==========")

            if hasattr(e, "status_code"):
                print("Status Code:", e.status_code)

            if hasattr(e, "body"):
                print("Response Body:", e.body)

            if hasattr(e, "headers"):
                print("Headers:", e.headers)

            print("Exception:", str(e))
            print("====================================")

            raise