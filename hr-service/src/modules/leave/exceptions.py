from fastapi import status

from src.core.exceptions import WorkPilotException


class LeaveTypeNotFoundException(WorkPilotException):
    """Raised when a leave type is not found."""

    def __init__(self):
        super().__init__(
            message="Leave type not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class LeaveTypeAlreadyExistsException(WorkPilotException):
    """Raised when a leave type with the same name or code already exists."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )

class ResourceNotFoundException(WorkPilotException):
    """Raised when a leave resource is not found."""

    def __init__(self, message: str = "Resource not found."):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class BadRequestException(WorkPilotException):
    """Raised when the leave request is invalid."""

    def __init__(self, message: str = "Bad request."):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class LeaveBalanceNotFoundException(WorkPilotException):
    """Raised when a leave balance record is not found."""

    def __init__(self, message: str = "Leave balance record not found."):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )