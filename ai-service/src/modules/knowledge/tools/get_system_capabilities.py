"""
Get system capabilities tool for the Knowledge Agent.

This tool provides a dynamic registry list of all capabilities, domains, and counts of
registered tools in the system.
"""

from __future__ import annotations

from typing import Any
from modules.knowledge.registry import tool_registry
from modules.hr.registry import hr_tool_registry
from modules.it.registry import tool_registry as it_tool_registry


async def get_system_capabilities() -> dict[str, Any]:
    """
    Retrieve the registered specialist domains, tool categories, and active tools in the system.

    Returns:
        A dictionary containing description, tools count, and categories for each specialist domain.
    """
    
    hr_tools = hr_tool_registry.list_tools()
    it_tools = it_tool_registry.list_tools()
    knowledge_tools = tool_registry.list_tools()
    
    return {
        "domains": {
            "hr": {
                "description": "Manage employee profiles, leave requests, attendance, organization structure (departments, branches, designations), and HR policies.",
                "tools_count": len(hr_tools),
                "categories": ["employee management", "leave management", "attendance tracking", "organization setup", "policy administration"],
                "sample_tools": hr_tools[:5]
            },
            "it": {
                "description": "Manage IT assets, system maintenance, software installation, license assignment, and helpdesk support tickets.",
                "tools_count": len(it_tools),
                "categories": ["maintenance", "software management", "license tracking", "helpdesk ticketing"],
                "sample_tools": it_tools[:5]
            },
            "knowledge": {
                "description": "Access the organization's knowledge base, search documents, and query assistant capabilities.",
                "tools_count": len(knowledge_tools),
                "categories": ["document search", "capabilities retrieval"],
                "sample_tools": knowledge_tools[:5]
            }
        }
    }


# Register the tool
tool_registry.register(
    "get_system_capabilities",
    get_system_capabilities,
)
