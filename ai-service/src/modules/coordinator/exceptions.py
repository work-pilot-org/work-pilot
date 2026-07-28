# Coordinator exceptions
"""
Exceptions for the Coordinator Agent.

This module defines all custom exceptions used within the coordinator's
orchestration pipeline, ensuring errors are handled gracefully.
"""

class CoordinatorError(Exception):
    """Base exception for all errors originating in the coordinator module."""
    pass


class IntentDetectionError(CoordinatorError):
    """Raised when the Intent Detector fails to confidently classify the user's request."""
    pass


class UnknownDomainError(CoordinatorError):
    """Raised by the Router or Registry when requested to route to an unsupported domain."""
    
    def __init__(self, domain: str) -> None:
        self.domain = domain
        super().__init__(f"Unknown or unsupported domain agent requested: '{domain}'")


class PlannerError(CoordinatorError):
    """Raised when the Planner fails to generate a valid, structured execution plan."""
    pass


class ToolExecutionError(CoordinatorError):
    """
    Raised when the Tool Executor encounters an unrecoverable error 
    (e.g., timeout or crash) while invoking a specialist agent's tool.
    """
    
    def __init__(self, agent_name: str, message: str) -> None:
        self.agent_name = agent_name
        super().__init__(f"Tool execution failed while communicating with specialist agent '{agent_name}': {message}")
