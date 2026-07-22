from src.core.exceptions import NotFoundException, BadRequestException, ForbiddenException


class WorkflowNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(detail="Workflow template not found")


class WorkflowStepNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(detail="Workflow step not found")


class WorkflowExecutionNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(detail="Workflow execution not found")


class TaskNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(detail="Approval task not found")


class InvalidWorkflowStateException(BadRequestException):
    def __init__(self, detail: str = "Invalid workflow state transition"):
        super().__init__(detail=detail)


class UnauthorizedApproverException(ForbiddenException):
    def __init__(self):
        super().__init__()
