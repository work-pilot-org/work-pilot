"""
Knowledge Agent tools.

Importing this package loads all Knowledge Agent tool modules
and registers their handlers with the Knowledge Tool Registry.
"""

from modules.knowledge.tools import (
    search_documents,
    search_faq,
    search_policies,
    get_system_capabilities,
)

__all__ = [
    "search_documents",
    "search_faq",
    "search_policies",
    "get_system_capabilities",
]