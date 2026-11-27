"""
Tool definitions for the WorkPilot Analytics Agent.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from google.genai import types
from pydantic import TypeAdapter

from core.logger import get_logger
from modules.analytics.registry import analytics_tool_registry

# Import handlers so their registration code executes.
import modules.analytics.handlers  # noqa: F401

logger = get_logger(__name__)

TOOL_DESCRIPTIONS: dict[str, str] = {
    "get_attendance_summary": "Answers questions about attendance rate, total worked hours, and overtime metrics.",
    "get_leave_utilization": "Answers questions about leave requests, pending approvals, and leave utilization. Can filter by period and department.",
    "get_headcount": "Answers questions about active employees, headcount by department, and employment type distributions.",
    "get_ticket_summary": "Answers questions about open IT tickets, resolution times, and ticket volumes.",
    "get_asset_assignments": "Answers questions about IT asset assignments and statuses.",
    "get_workflow_performance": "Answers questions about workflow execution performance.",
    "get_workflow_bottlenecks": "Answers questions about bottlenecks and pending steps in workflows.",
}

def _inline_schema_refs(schema: dict[str, Any]) -> dict[str, Any]:
    definitions = schema.get("$defs", {})

    def resolve(value: Any) -> Any:
        if isinstance(value, dict):
            if "anyOf" in value:
                non_null_types = [item for item in value["anyOf"] if item.get("type") != "null"]
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
                    raise ValueError(f"Unsupported schema reference: {ref}")
                definition_name = ref[len(prefix):]
                if definition_name not in definitions:
                    raise ValueError(f"Schema definition not found: {definition_name}")
                resolved_definition = resolve(definitions[definition_name])
                siblings = {}
                for k, v in value.items():
                    if k in ("$ref", "additionalProperties", "additional_properties", "title", "default"):
                        continue
                    if k == "properties":
                        siblings[k] = {prop_name: resolve(prop_schema) for prop_name, prop_schema in v.items()}
                    else:
                        siblings[k] = resolve(v)
                return {**resolved_definition, **siblings}

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
            return [resolve(item) for item in value]
        return value

    return resolve(schema)

def _build_parameter_schema(handler: Any) -> dict[str, Any]:
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
        annotation = type_hints.get(name, parameter.annotation)
        if annotation is inspect.Parameter.empty:
            raise TypeError(f"Tool parameter '{name}' on '{handler.__name__}' has no type annotation.")
        
        pydantic_schema = TypeAdapter(annotation).json_schema()
        properties[name] = _inline_schema_refs(pydantic_schema)
        
        if parameter.default is inspect.Parameter.empty:
            required.append(name)

    schema: dict[str, Any] = {
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required
    return schema

def get_analytics_tool_definitions() -> list[types.Tool]:
    declarations: list[types.FunctionDeclaration] = []

    for tool_name in analytics_tool_registry.list_tools():
        handler = analytics_tool_registry.get(tool_name)
        description = TOOL_DESCRIPTIONS.get(
            tool_name,
            inspect.getdoc(handler) or f"Execute Analytics operation '{tool_name}'."
        )

        declarations.append(
            types.FunctionDeclaration(
                name=tool_name,
                description=description,
                parameters=_build_parameter_schema(handler),
            )
        )

    logger.info("Analytics tool definitions created", tool_count=len(declarations))
    
    if not declarations:
        return []
        
    return [types.Tool(function_declarations=declarations)]
