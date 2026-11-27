"""
Tests for IT Agent tool registration and definitions.
"""

import modules.it.tools  # noqa: F401
from modules.it.registry import tool_registry
from modules.it.tool_definitions import get_it_tool_definitions


def test_it_tools_are_registered():
    tools = tool_registry.list_tools()

    assert tools
    assert "create_ticket" in tools
    assert "list_assets" in tools
    assert "assign_device" in tools
    assert "install_software" in tools
    assert "assign_license" in tools
    assert "create_access_request" in tools
    assert "complete_maintenance" in tools


def test_tool_definitions_match_registry():
    tools = get_it_tool_definitions()

    assert len(tools) == 1

    declarations = tools[0].function_declarations or []

    registered_names = set(tool_registry.list_tools())
    declared_names = {
        declaration.name
        for declaration in declarations
    }

    assert declared_names == registered_names