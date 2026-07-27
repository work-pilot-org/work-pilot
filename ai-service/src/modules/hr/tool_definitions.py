"""
Tool definitions for the WorkPilot HR Agent.

Generates Gemini function declarations directly from the registered
HR tools and their Python/Pydantic type annotations.
"""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints

from google.genai import types
from pydantic import TypeAdapter

from core.logger import get_logger
from modules.hr.registry import hr_tool_registry

# Import all HR tool modules so their registration code executes.
import modules.hr.tools  # noqa: F401

logger = get_logger(__name__)


TOOL_DESCRIPTIONS: dict[str, str] = {

    # =====================================================
    # Employee
    # =====================================================

    "create_employee": "Create a new employee.",
    "get_all_employees": "Retrieve all employees.",
    "get_employee": "Retrieve an employee by ID.",
    "update_employee": "Update employee details.",
    "delete_employee": "Delete an employee.",
    "search_employee": "Search employees.",

    "get_employee_profile": "Retrieve an employee profile.",
    "update_employee_profile": "Update an employee profile.",

    "upload_document": "Upload an employee document.",
    "get_documents": "Retrieve employee documents.",
    "delete_document": "Delete an employee document.",

    # =====================================================
    # Attendance
    # =====================================================

    "check_in": "Check in an employee.",
    "check_out": "Check out an employee.",

    "create_attendance": "Create an attendance record.",
    "get_all_attendance": "Retrieve attendance records.",
    "get_attendance": "Retrieve an attendance record.",
    "update_attendance": "Update attendance.",
    "delete_attendance": "Delete attendance.",

    "get_employee_attendance": "Retrieve employee attendance.",
    "attendance_summary": "Retrieve attendance summary.",
    "get_attendance_by_date": "Retrieve attendance by date.",
    "today_attendance": "Retrieve today's attendance.",
    "get_active_attendance": "Retrieve active attendance.",
    "update_attendance_status": "Update attendance status.",
    "monthly_report": "Generate attendance report.",
    "export_attendance": "Export attendance.",

    # =====================================================
    # Leave
    # =====================================================

    "create_leave_type": "Create a leave type.",
    "get_leave_types": "Retrieve leave types.",
    "get_leave_type": "Retrieve a leave type.",
    "update_leave_type": "Update a leave type.",
    "delete_leave_type": "Delete a leave type.",

    "create_leave_request": "Create a leave request.",
    "get_leave_requests": "Retrieve leave requests.",
    "get_leave_request": "Retrieve a leave request.",
    "update_leave_request": "Update a leave request.",
    "update_leave_request_status": "Approve or reject a leave request.",
    "delete_leave_request": "Delete a leave request.",

    "employee_leave_requests": "Retrieve employee leave requests.",
    "employee_leave_balance": "Retrieve employee leave balance.",
    "employee_leave_summary": "Retrieve employee leave summary.",

    "create_leave_balance": "Create leave balance.",
    "get_leave_balances": "Retrieve leave balances.",
    "get_leave_balance": "Retrieve leave balance.",
    "update_leave_balance": "Update leave balance.",
    "delete_leave_balance": "Delete leave balance.",

    "leave_report": "Generate organization leave report.",
    "monthly_leave_report": "Generate monthly leave report.",
    "department_leave_report": "Generate department leave report.",
    "leave_calendar": "Retrieve leave calendar.",

    "create_holiday": "Create a holiday.",
    "get_holidays": "Retrieve holidays.",
    "delete_holiday": "Delete a holiday.",

    # =====================================================
    # Organization
    # =====================================================

    "create_department": "Create a department.",
    "get_departments": "Retrieve departments.",
    "update_department": "Update a department.",
    "delete_department": "Delete a department.",

    "create_designation": "Create a designation.",
    "get_designations": "Retrieve designations.",
    "update_designation": "Update a designation.",
    "delete_designation": "Delete a designation.",

    "create_branch": "Create a branch.",
    "get_branches": "Retrieve branches.",
    "update_branch": "Update a branch.",
    "delete_branch": "Delete a branch.",

    "create_shift": "Create a shift.",
    "get_shifts": "Retrieve shifts.",
    "update_shift": "Update a shift.",
    "delete_shift": "Delete a shift.",

    # =====================================================
    # Policies
    # =====================================================

    "create_leave_policy": "Create a leave policy.",
    "get_leave_policies": "Retrieve leave policies.",
    "get_leave_policy": "Retrieve a leave policy.",
    "update_leave_policy": "Update a leave policy.",
    "delete_leave_policy": "Delete a leave policy.",

    "create_attendance_policy": "Create an attendance policy.",
    "get_attendance_policies": "Retrieve attendance policies.",
    "get_attendance_policy": "Retrieve an attendance policy.",
    "update_attendance_policy": "Update an attendance policy.",
    "delete_attendance_policy": "Delete an attendance policy.",

    "create_shift_policy": "Create a shift policy.",
    "get_shift_policies": "Retrieve shift policies.",
    "get_shift_policy": "Retrieve a shift policy.",
    "update_shift_policy": "Update a shift policy.",
    "delete_shift_policy": "Delete a shift policy.",

    "create_holiday_policy": "Create a holiday policy.",
    "get_holiday_policies": "Retrieve holiday policies.",
    "get_holiday_policy": "Retrieve a holiday policy.",
    "update_holiday_policy": "Update a holiday policy.",
    "delete_holiday_policy": "Delete a holiday policy.",

    "create_probation_policy": "Create a probation policy.",
    "get_probation_policies": "Retrieve probation policies.",
    "get_probation_policy": "Retrieve a probation policy.",
    "update_probation_policy": "Update a probation policy.",
    "delete_probation_policy": "Delete a probation policy.",
}


# KEEP THESE TWO FUNCTIONS EXACTLY THE SAME AS THE IT AGENT
# ---------------------------------------------------------
# Copy _inline_schema_refs() exactly from your IT file.
# Copy _build_parameter_schema() exactly from your IT file.
# ---------------------------------------------------------


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
                    if key != "$ref"
                }

                return {
                    **resolved_definition,
                    **siblings,
                }

            return {
                key: resolve(item)
                for key, item in value.items()
                if key != "$defs"
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


def get_hr_tool_definitions() -> list[types.Tool]:
    """
    Generate Gemini function declarations for every registered HR tool.
    """

    declarations: list[types.FunctionDeclaration] = []

    for tool_name in hr_tool_registry.list_tools():

        handler = hr_tool_registry.get(tool_name)

        description = TOOL_DESCRIPTIONS.get(
            tool_name,
            inspect.getdoc(handler)
            or f"Execute HR operation '{tool_name}'.",
        )

        declarations.append(
            types.FunctionDeclaration(
                name=tool_name,
                description=description,
                parameters=_build_parameter_schema(handler),
            )
        )

    logger.info(
        "HR tool definitions created",
        tool_count=len(declarations),
    )

    return [
        types.Tool(
            function_declarations=declarations,
        )
    ]