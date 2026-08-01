"""
Tool registry for the WorkPilot HR Agent.

Maintains a registry of all HR tools that can be invoked by the LLM.
"""

from __future__ import annotations

from typing import Any, Callable

from core.logger import get_logger

logger = get_logger(__name__)


class HRToolRegistry:
    """
    Registry for HR tools.

    Responsibilities:
    - Register HR tool handlers.
    - Retrieve registered tools.
    - Check tool existence.
    - List available tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
    ) -> None:
        """
        Register a tool.

        Args:
            name:
                Unique tool name.

            handler:
                Python function implementing the tool.
        """

        if name in self._tools:
            raise ValueError(
                f"HR tool '{name}' is already registered."
            )

        self._tools[name] = handler

        logger.info(
            "Registered HR tool",
            tool_name=name,
        )

    def get(
        self,
        name: str,
    ) -> Callable[..., Any]:
        """
        Retrieve a registered tool.
        """

        try:
            return self._tools[name]

        except KeyError as exc:
            raise KeyError(
                f"Unknown HR tool: {name}"
            ) from exc

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a tool exists.
        """

        return name in self._tools

    def list_tools(self) -> list[str]:
        """
        Return all registered tool names.
        """

        return sorted(self._tools.keys())

    def clear(self) -> None:
        """
        Remove all registered tools.

        Useful for testing.
        """

        self._tools.clear()

        logger.info("Cleared HR tool registry")


hr_tool_registry = HRToolRegistry()