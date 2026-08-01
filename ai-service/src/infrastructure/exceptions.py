"""
Custom exceptions for infrastructure components.

These exceptions are shared by all service clients
(IT, HR, Workflow, etc.) when communicating with
external microservices.
"""

from __future__ import annotations


class InfrastructureError(Exception):
    """
    Base exception for all infrastructure-related errors.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ServiceUnavailableError(InfrastructureError):
    """
    Raised when an external service is unavailable.
    """


class RequestTimeoutError(InfrastructureError):
    """
    Raised when an HTTP request exceeds the configured timeout.
    """


class AuthenticationError(InfrastructureError):
    """
    Raised when authentication with an external service fails.
    """


class AuthorizationError(InfrastructureError):
    """
    Raised when the caller is not authorized.
    """


class ResourceNotFoundError(InfrastructureError):
    """
    Raised when a requested resource does not exist.
    """


class BadRequestError(InfrastructureError):
    """
    Raised when invalid data is sent to an external service.
    """


class ConflictError(InfrastructureError):
    """
    Raised when a resource already exists or conflicts
    with the current request.
    """


class ExternalServiceError(InfrastructureError):
    """
    Raised for unexpected external service failures.
    """