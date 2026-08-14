from enum import Enum


class Channel(str, Enum):
    EMAIL = "email"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class NotificationType(str, Enum):
    PASSWORD_RESET = "password_reset"
    INVITATION = "invitation"
    WORKFLOW_APPROVAL = "workflow_approval"
