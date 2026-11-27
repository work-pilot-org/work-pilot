"""
Shared FastAPI dependencies.
"""

from __future__ import annotations

from modules.coordinator.agent import (
    CoordinatorAgent,
    coordinator_agent,
)


def get_coordinator() -> CoordinatorAgent:
    """
    Return the singleton Coordinator Agent.
    """
    return coordinator_agent