"""
Tool definitions for the WorkPilot IT Agent.

Generates Gemini function declarations directly from the registered
IT tools and their Python/Pydantic type annotations.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from google.genai import types
from pydantic import TypeAdapter

# Import all tool modules so their registration code executes.
import modules.it.tools  # noqa: F401
from core.logger import get_logger
from modules.it.registry import tool_registry

logger = get_logger(__name__)


TOOL_DESCRIPTIONS: dict[str, str] = {
    # Help Desk
    "create_ticket": "Create a new IT help desk ticket.",
    "list_tickets": "List IT help desk tickets.",
    "get_ticket": "Retrieve a help desk ticket by its ID.",
    "update_ticket": "Update an existing help desk ticket.",
    "assign_ticket": "Assign a help desk ticket to a technician.",

    # Assets
    "create_asset": "Create a new IT asset.",
    "list_assets": (
        "List or search IT assets, optionally filtering by category, "
        "status, assigned user, or search text."
    ),
    "get_asset": "Retrieve an IT asset by its UUID.",
    "update_asset": "Update an existing IT asset.",
    "delete_asset": "Delete an IT asset.",
    "assign_asset": "Assign an IT asset to a user.",
    "return_asset": "Return an assigned IT asset.",

    # Devices
    "create_device": "Create a new device.",
    "list_devices": "List devices managed by WorkPilot IT.",
    "get_device": "Retrieve a device by its UUID.",
    "update_device": "Update an existing device.",
    "delete_device": "Delete a device.",
    "assign_device": "Assign a device to a user.",
    "return_device": "Return an assigned device.",
    "add_maintenance_log": (
        "Add a maintenance history entry for a device."
    ),
    "get_maintenance_history": (
        "Retrieve the maintenance history of a device."
    ),

    # Software
    "create_software": "Create a software record.",
    "list_software": "List software managed by WorkPilot IT.",
    "get_software": "Retrieve software details by UUID.",
    "update_software": "Update an existing software record.",
    "delete_software": "Delete a software record.",
    "install_software": (
        "Install software for a device or user."
    ),
    "uninstall_software": (
        "Remove an existing software installation."
    ),
    "list_device_installations": (
        "List software installations for a device."
    ),
    "list_user_installations": (
        "List software installations for a user."
    ),
    "create_installation_request": (
        "Create a software installation request."
    ),
    "list_installation_requests": (
        "List software installation requests."
    ),
    "get_installation_request": (
        "Retrieve a software installation request by UUID."
    ),

    # Licenses
    "create_license": "Create a software license.",
    "list_licenses": "List software licenses.",
    "get_license": "Retrieve a software license by UUID.",
    "update_license": "Update a software license.",
    "delete_license": "Delete a software license.",
    "assign_license": "Assign a software license to a user.",
    "return_license": (
        "Return or revoke an assigned software license."
    ),
    "list_license_assignments": (
        "List assignments associated with a software license."
    ),

    # Access
    "create_access_request": "Create an IT access request.",
    "list_access_requests": "List IT access requests.",
    "get_access_request": "Retrieve an access request by UUID.",
    "update_access_request": "Update an access request.",
    "update_access_status": (
        "Change the status of an access request."
    ),
    "delete_access_request": "Delete an access request.",

    # Maintenance
    "create_maintenance_record": (
        "Create a device maintenance record."
    ),
    "list_maintenance_records": "List maintenance records.",
    "get_maintenance_record": (
        "Retrieve a maintenance record by UUID."
    ),
    "update_maintenance_record": (
        "Update a maintenance record."
    ),
    "delete_maintenance_record": (
        "Delete a maintenance record."
    ),
    "complete_maintenance": (
        "Mark a maintenance record as completed."
    ),
    "list_device_maintenance": (
        "List maintenance records for a device."
    ),
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

                # Preserve any sibling fields beside $ref.
                siblings = {
                    key: resolve(item)
                    for key, item in value.items()
                    if key not in ("$ref", "additionalProperties", "additional_properties", "title")
                }

                return {
                    **resolved_definition,
                    **siblings,
                }

            return {
                key: resolve(item)
                for key, item in value.items()
                if key not in ("$defs", "additionalProperties", "additional_properties", "title")
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

def get_it_tool_definitions() -> list[types.Tool]:
    """
    Generate Gemini function declarations for every registered IT tool.
    """

    declarations: list[types.FunctionDeclaration] = []

    for tool_name in tool_registry.list_tools():

        handler = tool_registry.get(tool_name)

        description = TOOL_DESCRIPTIONS.get(
            tool_name,
            inspect.getdoc(handler)
            or f"Execute IT operation '{tool_name}'.",
        )

        declarations.append(
            types.FunctionDeclaration(
                name=tool_name,
                description=description,
                parameters=_build_parameter_schema(handler),
            )
        )

    logger.info(
        "IT tool definitions created",
        tool_count=len(declarations),
    )

    return [
        types.Tool(
            function_declarations=declarations,
        )
    ]