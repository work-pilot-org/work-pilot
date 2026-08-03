from shared_infrastructure.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    ResourceNotFoundException,
)


class WorkflowNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(message="Workflow template not found")


class WorkflowStepNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(message="Workflow step not found")


class WorkflowExecutionNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(message="Workflow execution not found")


class TaskNotFoundException(ResourceNotFoundException):
    def __init__(self):
        super().__init__(message="Approval task not found")


class InvalidWorkflowStateException(BadRequestException):
    def __init__(self, detail: str = "Invalid workflow state transition"):
        super().__init__(detail=detail)


class UnauthorizedApproverException(ForbiddenException):
    def __init__(self):
        super().__init__()
