from enum import Enum


class ActivityAction(str, Enum):
    """
    Defines all supported Help Desk activity actions.

    Used for audit logging, notifications,
    analytics, and future AI event processing.
    """

    # Ticket Lifecycle
    TICKET_CREATED = "TICKET_CREATED"
    TICKET_UPDATED = "TICKET_UPDATED"
    TICKET_DELETED = "TICKET_DELETED"

    # Status
    STATUS_CHANGED = "STATUS_CHANGED"

    # Assignment
    ASSIGNED = "ASSIGNED"
    UNASSIGNED = "UNASSIGNED"

    # Priority
    PRIORITY_CHANGED = "PRIORITY_CHANGED"

    # Comments
    COMMENT_ADDED = "COMMENT_ADDED"
    COMMENT_UPDATED = "COMMENT_UPDATED"
    COMMENT_DELETED = "COMMENT_DELETED"

    # Attachments
    ATTACHMENT_UPLOADED = "ATTACHMENT_UPLOADED"
    ATTACHMENT_DELETED = "ATTACHMENT_DELETED"

    # Resolution
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    REOPENED = "REOPENED"