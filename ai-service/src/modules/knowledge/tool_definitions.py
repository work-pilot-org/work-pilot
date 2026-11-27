"""
Tool definitions for the WorkPilot Knowledge Agent.

Generates Gemini function declarations from the registered
Knowledge Agent tools.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from google.genai import types
from pydantic import TypeAdapter

import modules.knowledge.tools

from core.logger import get_logger
from modules.knowledge.registry import tool_registry

logger = get_logger(__name__)


# Parameters that must never be exposed to the LLM.
#
# These are application-controlled values. The LLM should only
# provide user-facing search arguments.
INTERNAL_PARAMETERS = {
    "headers",
    "tenant_id",
    "retriever",
}


TOOL_DESCRIPTIONS: dict[str, str] = {
    "search_documents": (
        "Search the organization's knowledge base for relevant "
        "documents and information."
    ),
    "search_faq": (
        "Search the organization's frequently asked questions "
        "for an answer."
    ),
    "search_policies": (
        "Search the organization's policies and procedures "
        "for relevant information."
    ),
    "get_system_capabilities": (
        "Retrieve the registered specialist domains, tool categories, and active tools in the system."
    ),
}


def _inline_schema_refs(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """
    Replace local Pydantic $ref references with their definitions.

    Gemini function declarations cannot directly consume
    Pydantic's local $defs/$ref structure.
    """

    definitions = schema.get("$defs", {})

    def resolve(value: Any) -> Any:
        if isinstance(value, dict):
            if "$ref" in value:
                ref = value["$ref"]
                prefix = "#/$defs/"

                if not ref.startswith(prefix):
                    raise ValueError(
                        f"Unsupported schema reference: {ref}"
                    )

                definition_name = ref[len(prefix):]

                if definition_name not in definitions:
                    raise ValueError(
                        f"Schema definition not found: "
                        f"{definition_name}"
                    )

                resolved_definition = resolve(
                    definitions[definition_name]
                )

                siblings = {
                    key: resolve(item)
                    for key, item in value.items()
                    if key not in {
                        "$ref",
                        "additionalProperties",
                        "additional_properties",
                        "title",
                    }
                }

                return {
                    **resolved_definition,
                    **siblings,
                }

            return {
                key: resolve(item)
                for key, item in value.items()
                if key not in {
                    "$defs",
                    "additionalProperties",
                    "additional_properties",
                    "title",
                }
            }

        if isinstance(value, list):
            return [
                resolve(item)
                for item in value
            ]

        return value

    return resolve(schema)


def _build_parameter_schema(
    handler: Any,
) -> dict[str, Any]:
    """
    Build a Gemini-compatible JSON schema for a registered
    Knowledge Agent tool.

    Internal parameters such as tenant_id and retriever are
    deliberately excluded because they are controlled by
    WorkPilot rather than the LLM.
    """

    signature = inspect.signature(handler)

    try:
        type_hints = get_type_hints(handler)
    except (NameError, TypeError):
        type_hints = {}

    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, parameter in signature.parameters.items():
        if name in INTERNAL_PARAMETERS:
            continue

        annotation = type_hints.get(
            name,
            parameter.annotation,
        )

        if annotation is inspect.Parameter.empty:
            raise TypeError(
                f"Tool parameter '{name}' on "
                f"'{handler.__name__}' has no type annotation."
            )

        pydantic_schema = TypeAdapter(
            annotation
        ).json_schema()

        properties[name] = _inline_schema_refs(
            pydantic_schema
        )

        if parameter.default is inspect.Parameter.empty:
            required.append(name)

    schema: dict[str, Any] = {
        "type": "object",
        "properties": properties,
    }

    if required:
        schema["required"] = required

    return schema


def get_knowledge_tool_definitions() -> list[types.Tool]:
    """
    Generate Gemini function declarations for all registered
    Knowledge Agent tools.
    """

    declarations: list[types.FunctionDeclaration] = []

    for tool_name in tool_registry.list_tools():
        handler = tool_registry.get(tool_name)

        description = TOOL_DESCRIPTIONS.get(
            tool_name,
            inspect.getdoc(handler)
            or f"Execute Knowledge operation '{tool_name}'.",
        )

        declarations.append(
            types.FunctionDeclaration(
                name=tool_name,
                description=description,
                parameters=_build_parameter_schema(handler),
            )
        )

    logger.info(
        "Knowledge tool definitions created",
        tool_count=len(declarations),
    )

    return [
        types.Tool(
            function_declarations=declarations,
        )
    ]