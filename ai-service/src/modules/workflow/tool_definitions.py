"""
Tool definitions for the WorkPilot Workflow Agent.

Generates Gemini function declarations directly from the registered
Workflow tools and their Python/Pydantic type annotations.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from google.genai import types
from pydantic import TypeAdapter

from core.logger import get_logger
from modules.workflow.registry import workflow_tool_registry

# Import all Workflow tool modules so their registration code executes.
import modules.workflow.tools  # noqa: F401

logger = get_logger(__name__)


TOOL_DESCRIPTIONS: dict[str, str] = {
    "create_workflow": "Create a new workflow.",
    "get_all_workflows": "Retrieve a list of all workflows.",
    "get_workflow": "Retrieve a specific workflow by its ID.",
    "update_workflow": "Update an existing workflow.",
    "delete_workflow": "Delete a workflow.",
    "start_workflow_execution": "Start a new workflow execution.",
    "get_workflow_executions": "Retrieve a list of all workflow executions.",
    "get_workflow_execution": "Retrieve a specific workflow execution by its ID.",
    "approve_task": "Approve or reject a task within a workflow execution.",
    "cancel_workflow": "Cancel an ongoing workflow execution.",
    "restart_workflow": "Restart a cancelled or failed workflow execution.",
    "get_workflow_history": "Retrieve the approval history of a workflow execution.",
}


def _inline_schema_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Replace local Pydantic $ref references with their actual definitions.

    Pydantic JSON Schema commonly uses:
        $defs
        $ref

    Gemini FunctionDeclaration parameters do not accept those fields,
    so references are resolved before passing the schema to Gemini.
    """

    definitions = schema.get("$defs", {})

    def resolve(value: Any) -> Any:
        if isinstance(value, dict):
            if "anyOf" in value:
                non_null_types = [
                    item for item in value["anyOf"]
                    if item.get("type") != "null"
                ]
                if non_null_types:
                    primary_type = resolve(non_null_types[0])
                    siblings = {}
                    for k, v in value.items():
                        if k in ("anyOf", "additionalProperties", "additional_properties", "title", "default"):
                            continue
                        if k == "properties":
                            siblings[k] = {prop_name: resolve(prop_schema) for prop_name, prop_schema in v.items()}
                        else:
                            siblings[k] = resolve(v)
                    if isinstance(primary_type, dict):
                        return {**primary_type, **siblings}
                    return primary_type

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
                        f"Schema definition not found: {definition_name}"
                    )

                resolved_definition = resolve(
                    definitions[definition_name]
                )

                siblings = {}
                for k, v in value.items():
                    if k in ("$ref", "additionalProperties", "additional_properties", "title", "default"):
                        continue
                    if k == "properties":
                        siblings[k] = {prop_name: resolve(prop_schema) for prop_name, prop_schema in v.items()}
                    else:
                        siblings[k] = resolve(v)

                return {
                    **resolved_definition,
                    **siblings,
                }

            result = {}
            for k, v in value.items():
                if k in ("$defs", "additionalProperties", "additional_properties", "title", "default"):
                    continue
                if k == "properties":
                    result[k] = {prop_name: resolve(prop_schema) for prop_name, prop_schema in v.items()}
                else:
                    result[k] = resolve(v)
            return result

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
    Generate Gemini-compatible JSON schema for one registered tool.

    `headers` is deliberately excluded because authentication and tenant
    context must come from WorkPilot, never from the LLM.
    """

    signature = inspect.signature(handler)

    try:
        type_hints = get_type_hints(handler)
    except (NameError, TypeError):
        type_hints = {}

    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, parameter in signature.parameters.items():
        if name == "headers":
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


def get_workflow_tool_definitions() -> list[types.Tool]:
    """
    Generate Gemini function declarations for every registered Workflow tool.
    """

    declarations: list[types.FunctionDeclaration] = []

    for tool_name in workflow_tool_registry.list_tools():

        handler = workflow_tool_registry.get(tool_name)

        description = TOOL_DESCRIPTIONS.get(
            tool_name,
            inspect.getdoc(handler)
            or f"Execute Workflow operation '{tool_name}'.",
        )

        declarations.append(
            types.FunctionDeclaration(
                name=tool_name,
                description=description,
                parameters=_build_parameter_schema(handler),
            )
        )

    logger.info(
        "Workflow tool definitions created",
        tool_count=len(declarations),
    )

    return [
        types.Tool(
            function_declarations=declarations,
        )
    ]
