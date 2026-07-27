"""
IT Agent tools.

Importing this package loads all IT tool modules and registers their
handlers with the IT Tool Registry.
"""

from modules.it.tools import (
    access,
    assets,
    devices,
    helpdesk,
    licenses,
    maintenance,
    software,
)

__all__ = [
    "access",
    "assets",
    "devices",
    "helpdesk",
    "licenses",
    "maintenance",
    "software",
]