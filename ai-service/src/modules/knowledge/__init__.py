"""
Knowledge Agent tools.

Importing this package loads all implemented Knowledge Agent
tool modules and registers their handlers with the Knowledge
Tool Registry.
"""

from modules.knowledge.tools import search_documents

__all__ = [
    "search_documents",
]