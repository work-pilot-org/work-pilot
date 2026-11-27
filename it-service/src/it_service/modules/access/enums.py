from enum import Enum


class AccessRequestType(str, Enum):
    VPN = "VPN"
    APPLICATION = "APPLICATION"
    DATABASE = "DATABASE"


class AccessRequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVOKED = "REVOKED"