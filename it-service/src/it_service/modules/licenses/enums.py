from enum import Enum

# ==========================================================
# License Type
# ==========================================================

class LicenseType(str, Enum):
    """
    Types of software licenses.
    """

    PERPETUAL = "Perpetual"
    SUBSCRIPTION = "Subscription"
    TRIAL = "Trial"
    OPEN_SOURCE = "Open Source"
    FREE = "Free"


# ==========================================================
# License Status
# ==========================================================

class LicenseStatus(str, Enum):
    """
    Current status of the license.
    """

    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    EXPIRED = "Expired"
    REVOKED = "Revoked"


# ==========================================================
# Renewal Status
# ==========================================================

class RenewalStatus(str, Enum):
    """
    Renewal status of the license.
    """

    ACTIVE = "Active"
    RENEWAL_DUE = "Renewal Due"
    RENEWED = "Renewed"
    EXPIRED = "Expired"