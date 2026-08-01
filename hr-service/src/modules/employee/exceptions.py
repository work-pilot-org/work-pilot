from fastapi import status

from src.core.exceptions import WorkPilotException


class EmployeeNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )


class EmployeeAlreadyExistsException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee already exists for this Auth user.",
        )


class EmployeeCodeAlreadyExistsException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists.",
        )


class EmployeeProfileNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )


class EmployeeDocumentNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee document not found.",
        )