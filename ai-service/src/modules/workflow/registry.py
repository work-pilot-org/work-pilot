"""
Tool registry for the WorkPilot Workflow Agent.

Maintains a registry of all Workflow tools that can be invoked by the LLM.
"""

from __future__ import annotations

from typing import Any, Callable

from core.logger import get_logger

logger = get_logger(__name__)


class WorkflowToolRegistry:
    """
    Registry for Workflow tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
    ) -> None:
        if name in self._tools:
            raise ValueError(
                f"Workflow tool '{name}' is already registered."
            )

        self._tools[name] = handler
        logger.info(
            "Registered Workflow tool",
            tool_name=name,
        )

    def get(self, name: str) -> Callable[..., Any]:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Workflow tool: {name}"
            ) from exc

    def exists(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return sorted(self._tools.keys())

    def clear(self) -> None:
        self._tools.clear()
        logger.info("Cleared Workflow tool registry")


workflow_tool_registry = WorkflowToolRegistry()
