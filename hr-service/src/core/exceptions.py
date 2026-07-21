from fastapi import HTTPException


class WorkPilotException(HTTPException):
    """
    Base exception class for the WorkPilot application.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
    ):
        super().__init__(
            status_code=status_code,
            detail=message,
        )


class ResourceNotFoundException(WorkPilotException):
    """
    Raised when a requested resource cannot be found.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
    ):
        super().__init__(
            message=message,
            status_code=404,
        )


class BadRequestException(WorkPilotException):
    """
    Raised when the request contains invalid data.
    """

    def __init__(
        self,
        message: str = "Bad request.",
    ):
        super().__init__(
            message=message,
            status_code=400,
        )


class ConflictException(WorkPilotException):
    """
    Raised when a resource already exists or conflicts with existing data.
    """

    def __init__(
        self,
        message: str = "Conflict occurred.",
    ):
        super().__init__(
            message=message,
            status_code=409,
        )


class UnauthorizedException(WorkPilotException):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Unauthorized.",
    ):
        super().__init__(
            message=message,
            status_code=401,
        )


class ForbiddenException(WorkPilotException):
    """
    Raised when the user does not have permission.
    """

    def __init__(
        self,
        message: str = "Forbidden.",
    ):
        super().__init__(
            message=message,
            status_code=403,
        )


class InternalServerException(WorkPilotException):
    """
    Raised when an unexpected server error occurs.
    """

    def __init__(
        self,
        message: str = "Internal server error.",
    ):
        super().__init__(
            message=message,
            status_code=500,
        )