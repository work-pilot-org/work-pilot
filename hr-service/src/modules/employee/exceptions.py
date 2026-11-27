from fastapi import status

from shared_infrastructure.core.exceptions import WorkPilotException


class EmployeeNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Employee not found.",
        )


class EmployeeAlreadyExistsException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message="Employee already exists for this Auth user.",
        )


class EmployeeCodeAlreadyExistsException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message="Employee code already exists.",
        )


class EmployeeProfileNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Employee profile not found.",
        )


class EmployeeDocumentNotFoundException(WorkPilotException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Employee document not found.",
        )