"""
Tool execution layer for the Analytics Agent.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from pydantic import TypeAdapter, ValidationError

from core.logger import get_logger
from modules.analytics.registry import analytics_tool_registry

logger = get_logger(__name__)


class AnalyticsToolExecutionError(Exception):
    """Raised when an Analytics tool cannot be executed successfully."""


class AnalyticsToolExecutor:
    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        headers: dict[str, str] | None = None,
    ) -> Any:
        arguments = arguments or {}

        logger.info("Preparing Analytics tool execution", tool_name=tool_name)

        if not analytics_tool_registry.exists(tool_name):
            logger.warning("LLM requested unknown Analytics tool", tool_name=tool_name)
            raise AnalyticsToolExecutionError(f"Unknown Analytics tool: {tool_name}")

        handler = analytics_tool_registry.get(tool_name)

        try:
            validated_arguments = self._validate_arguments(
                handler=handler,
                arguments=arguments,
            )

            signature = inspect.signature(handler)
            if "headers" in signature.parameters:
                validated_arguments["headers"] = headers

            logger.info("Executing Analytics tool", tool_name=tool_name)
            result = handler(**validated_arguments)
            if inspect.isawaitable(result):
                result = await result

            logger.info("Analytics tool execution completed", tool_name=tool_name)
            return result

        except AnalyticsToolExecutionError:
            raise
        except ValidationError as exc:
            logger.warning("Invalid Analytics tool arguments", tool_name=tool_name, error=str(exc))
            raise AnalyticsToolExecutionError(f"Invalid arguments for Analytics tool '{tool_name}'.") from exc
        except TypeError as exc:
            logger.warning("Unable to call Analytics tool", tool_name=tool_name, error=str(exc))
            raise AnalyticsToolExecutionError(f"Invalid arguments for Analytics tool '{tool_name}'.") from exc
        except Exception as exc:
            logger.exception("Analytics tool execution failed", tool_name=tool_name, error=str(exc))
            raise AnalyticsToolExecutionError(f"Analytics tool '{tool_name}' failed.") from exc

    @staticmethod
    def _validate_arguments(
        *,
        handler: Any,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        signature = inspect.signature(handler)

        try:
            type_hints = get_type_hints(handler)
        except (NameError, TypeError):
            type_hints = {}

        allowed_arguments = {
            name
            for name in signature.parameters
            if name != "headers"
        }

        unknown_arguments = set(arguments) - allowed_arguments
        if unknown_arguments:
            unknown = ", ".join(sorted(unknown_arguments))
            raise AnalyticsToolExecutionError(f"Unexpected arguments for Analytics tool: {unknown}")

        validated: dict[str, Any] = {}
        for name, parameter in signature.parameters.items():
            if name == "headers":
                continue

            if name not in arguments:
                if parameter.default is inspect.Parameter.empty:
                    raise AnalyticsToolExecutionError(f"Missing required argument: {name}")
                continue

            value = arguments[name]
            annotation = type_hints.get(name, parameter.annotation)

            if annotation is inspect.Parameter.empty:
                validated[name] = value
                continue

            validated[name] = TypeAdapter(annotation).validate_python(value)

        return validated


analytics_tool_executor = AnalyticsToolExecutor()
