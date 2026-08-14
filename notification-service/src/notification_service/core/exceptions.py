import structlog
from shared_infrastructure.core.config import settings

logger = structlog.get_logger(__name__)


class NotificationEmailError(Exception):
    """Base exception for email delivery failures in Notification Service."""
    pass


class EmailConfigurationError(NotificationEmailError):
    """Raised when email provider credentials or parameters are misconfigured."""
    pass


class EmailDeliveryError(NotificationEmailError):
    """Raised when SendGrid API or delivery client fails to process requests."""
    pass
