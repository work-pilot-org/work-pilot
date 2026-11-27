"""
Tool registry for the IT Agent.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

ToolHandler = Callable[..., Awaitable[Any]]


class ToolRegistry:
    """
    Registry for IT Agent tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(
        self,
        name: str,
        handler: ToolHandler,
    ) -> None:
        """
        Register a tool.
        """
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")

        self._tools[name] = handler

    def get(self, name: str) -> ToolHandler:
        """
        Return a registered tool.
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered.")

        return self._tools[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return name in self._tools

    def list_tools(self) -> list[str]:
        """
        Return all registered tool names.
        """
        return sorted(self._tools.keys())


tool_registry = ToolRegistry()