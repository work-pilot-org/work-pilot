"""
Base interface for LLM providers.

Provider implementations handle communication with an LLM API.
Business logic and tool execution remain outside this layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    """Abstract contract implemented by every LLM provider."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
    ) -> str:
        """Generate a plain text response."""
        raise NotImplementedError

    @abstractmethod
    async def generate_with_tools(
        self,
        contents: Any,
        *,
        tools: list[Any],
        system_instruction: str | None = None,
    ) -> Any:
        """
        Generate a response with tool/function calling enabled.

        `contents` may contain either a simple user prompt or complete
        provider conversation history required for a tool-call round trip.
        """
        raise NotImplementedError