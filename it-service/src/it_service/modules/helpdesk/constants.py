"""
Constants used by the Help Desk module.

These values are shared across the service layer,
repository layer, and router layer.
"""

# -------------------------------------------------------------------
# Ticket Number
# -------------------------------------------------------------------

TICKET_PREFIX = "IT"

# -------------------------------------------------------------------
# Pagination
# -------------------------------------------------------------------

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------

MAX_TITLE_LENGTH = 150
MAX_DESCRIPTION_LENGTH = 5000

# -------------------------------------------------------------------
# Attachments
# -------------------------------------------------------------------

MAX_ATTACHMENT_SIZE_MB = 10

ALLOWED_ATTACHMENT_TYPES = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "doc",
    "docx",
    "xlsx",
    "txt",
}

# -------------------------------------------------------------------
# Search
# -------------------------------------------------------------------

MIN_SEARCH_LENGTH = 2
MAX_SEARCH_LENGTH = 100

# -------------------------------------------------------------------
# Default Values
# -------------------------------------------------------------------

DEFAULT_PRIORITY = "MEDIUM"
DEFAULT_STATUS = "OPEN"
DEFAULT_CATEGORY = "OTHER"

# -------------------------------------------------------------------
# Error Messages
# -------------------------------------------------------------------

TICKET_NOT_FOUND = "Ticket not found."

INVALID_TICKET_STATUS = "Invalid ticket status."

INVALID_PRIORITY = "Invalid ticket priority."

INVALID_CATEGORY = "Invalid ticket category."

ATTACHMENT_TOO_LARGE = "Attachment exceeds the maximum allowed size."

INVALID_ATTACHMENT_TYPE = "Attachment type is not supported."