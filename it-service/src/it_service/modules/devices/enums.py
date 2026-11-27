from enum import Enum


class DeviceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    REPAIR = "REPAIR"
    RETIRED = "RETIRED"