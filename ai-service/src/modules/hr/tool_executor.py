"""
Tool execution layer for the HR Agent.

Receives function calls selected by the LLM, validates their arguments
against the registered Python tool signature, and executes the tool
through the HR Tool Registry.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from pydantic import TypeAdapter, ValidationError

from core.logger import get_logger
from modules.hr.registry import hr_tool_registry

logger = get_logger(__name__)


class HRToolExecutionError(Exception):
    """Raised when an HR tool cannot be executed successfully."""


class HRToolExecutor:
    """
    Executes HR tools requested by the LLM.

    Responsibilities:
    - Verify that the requested tool exists.
    - Validate and convert LLM-generated arguments.
    - Execute the registered async tool.
    - Return the result to the agent.
    """

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Execute a registered HR tool.
        """

        arguments = arguments or {}

        logger.info(
            "Preparing HR tool execution",
            tool_name=tool_name,
        )

        if not hr_tool_registry.exists(tool_name):
            logger.warning(
                "LLM requested unknown HR tool",
                tool_name=tool_name,
            )

            raise HRToolExecutionError(
                f"Unknown HR tool: {tool_name}"
            )

        handler = hr_tool_registry.get(tool_name)

        try:
            validated_arguments = self._validate_arguments(
                handler=handler,
                arguments=arguments,
            )

            signature = inspect.signature(handler)

            if "headers" in signature.parameters:
                validated_arguments["headers"] = headers

            logger.info(
                "Executing HR tool",
                tool_name=tool_name,
            )

            result = handler(**validated_arguments)

            if inspect.isawaitable(result):
                result = await result

            logger.info(
                "HR tool execution completed",
                tool_name=tool_name,
            )

            return result

        except HRToolExecutionError:
            raise

        except ValidationError as exc:
            logger.warning(
                "Invalid HR tool arguments",
                tool_name=tool_name,
                error=str(exc),
            )

            raise HRToolExecutionError(
                f"Invalid arguments for HR tool '{tool_name}'."
            ) from exc

        except TypeError as exc:
            logger.warning(
                "Unable to call HR tool",
                tool_name=tool_name,
                error=str(exc),
            )

            raise HRToolExecutionError(
                f"Invalid arguments for HR tool '{tool_name}'."
            ) from exc

        except Exception as exc:
            logger.exception(
                "HR tool execution failed",
                tool_name=tool_name,
                error=str(exc),
            )

            raise HRToolExecutionError(
                f"HR tool '{tool_name}' failed."
            ) from exc

    @staticmethod
    def _validate_arguments(
        *,
        handler: Any,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate LLM arguments using the handler's Python annotations.
        """

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

            raise HRToolExecutionError(
                f"Unexpected arguments for HR tool: {unknown}"
            )

        validated: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():

            if name == "headers":
                continue

            if name not in arguments:

                if parameter.default is inspect.Parameter.empty:
                    raise HRToolExecutionError(
                        f"Missing required argument: {name}"
                    )

                continue

            value = arguments[name]

            annotation = type_hints.get(
                name,
                parameter.annotation,
            )

            if annotation is inspect.Parameter.empty:
                validated[name] = value
                continue

            validated[name] = TypeAdapter(
                annotation
            ).validate_python(value)

        return validated


hr_tool_executor = HRToolExecutor()