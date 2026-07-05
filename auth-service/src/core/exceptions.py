class WorkPilotException(Exception):
    """
    Base exception for the application.
    """

    pass


class CompanyAlreadyExistsException(WorkPilotException):
    """
    Raised when a company is already registered.
    """

    pass


class DomainAlreadyExistsException(WorkPilotException):
    """
    Raised when a domain already exists.
    """

    pass


class EmailAlreadyExistsException(WorkPilotException):
    """
    Raised when a user email already exists.
    """

    pass


class TenantNotFoundException(WorkPilotException):
    """
    Raised when a tenant cannot be found.
    """

    pass


class UserNotFoundException(WorkPilotException):
    """
    Raised when a user cannot be found.
    """

    pass


class InvalidCredentialsException(WorkPilotException):
    """
    Raised when login credentials are invalid.
    """

    pass


class EmployeeNotFoundException(WorkPilotException):
    """
    Raised when an employee cannot be found.
    """

    pass


class InvalidDomainException(WorkPilotException):
    """
    Raised when the requested domain is invalid.
    """

    pass