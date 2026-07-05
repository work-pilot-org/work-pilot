import pytest

from src.core.exceptions import (
    CompanyAlreadyExistsException,
    DomainAlreadyExistsException,
    EmailAlreadyExistsException,
    EmployeeNotFoundException,
    InvalidCredentialsException,
    InvalidDomainException,
    TenantNotFoundException,
    UserNotFoundException,
    WorkPilotException,
)

ALL_DOMAIN_EXCEPTIONS = [
    CompanyAlreadyExistsException,
    DomainAlreadyExistsException,
    EmailAlreadyExistsException,
    TenantNotFoundException,
    UserNotFoundException,
    InvalidCredentialsException,
    EmployeeNotFoundException,
    InvalidDomainException,
]


class TestWorkPilotException:
    def test_is_subclass_of_exception(self):
        assert issubclass(WorkPilotException, Exception)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(WorkPilotException):
            raise WorkPilotException("boom")

    def test_preserves_the_error_message(self):
        exc = WorkPilotException("something went wrong")

        assert str(exc) == "something went wrong"


@pytest.mark.parametrize("exception_class", ALL_DOMAIN_EXCEPTIONS)
class TestDomainExceptions:
    def test_is_subclass_of_workpilot_exception(self, exception_class):
        assert issubclass(exception_class, WorkPilotException)

    def test_is_subclass_of_exception(self, exception_class):
        assert issubclass(exception_class, Exception)

    def test_can_be_caught_via_base_workpilot_exception(self, exception_class):
        with pytest.raises(WorkPilotException):
            raise exception_class("test message")

    def test_can_be_caught_via_its_own_type(self, exception_class):
        with pytest.raises(exception_class):
            raise exception_class("test message")

    def test_preserves_the_error_message(self, exception_class):
        exc = exception_class("custom message")

        assert str(exc) == "custom message"

    def test_does_not_catch_sibling_exceptions(self, exception_class):
        siblings = [e for e in ALL_DOMAIN_EXCEPTIONS if e is not exception_class]

        for sibling in siblings:
            try:
                raise sibling("sibling error")
            except exception_class:
                pytest.fail(
                    f"{exception_class.__name__} should not catch "
                    f"{sibling.__name__}"
                )
            except sibling:
                pass