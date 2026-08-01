from enum import Enum


class TicketStatus(str, Enum):
    """
    Represents the lifecycle state of a help desk ticket.
    """

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class TicketPriority(str, Enum):
    """
    Represents the urgency of a help desk ticket.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketCategory(str, Enum):
    """
    Defines the type of issue reported.
    """

    HARDWARE = "HARDWARE"
    SOFTWARE = "SOFTWARE"
    NETWORK = "NETWORK"
    VPN = "VPN"
    ACCESS_CONTROL = "ACCESS_CONTROL"
    EMAIL = "EMAIL"
    SECURITY = "SECURITY"
    LICENSE = "LICENSE"
    PRINTER = "PRINTER"
    OTHER = "OTHER"


class TicketSource(str, Enum):
    """
    Defines where the ticket originated.
    """

    WEB = "WEB"
    MOBILE = "MOBILE"
    EMAIL = "EMAIL"
    AI_AGENT = "AI_AGENT"
    ADMIN = "ADMIN"


class TicketResolution(str, Enum):
    """
    Indicates how the ticket was resolved.
    """

    FIXED = "FIXED"
    WORKAROUND = "WORKAROUND"
    DUPLICATE = "DUPLICATE"
    CANNOT_REPRODUCE = "CANNOT_REPRODUCE"
    NOT_AN_ISSUE = "NOT_AN_ISSUE"