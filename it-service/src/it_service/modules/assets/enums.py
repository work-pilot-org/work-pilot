from enum import Enum


class AssetCategory(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    MONITOR = "MONITOR"
    PHONE = "PHONE"
    OTHER = "OTHER"


class AssetStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    DISPOSED = "DISPOSED"