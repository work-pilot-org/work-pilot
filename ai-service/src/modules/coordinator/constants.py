# Coordinator constants
"""
Constants for the Coordinator Agent.

This module centralizes all fixed values, Enum states, and configuration
constants used across the coordinator orchestration layer.
"""

from enum import Enum
from typing import Final, FrozenSet

# =============================================================================
# DOMAINS & AGENTS
# =============================================================================

class AgentDomain(str, Enum):
    """
    Supported specialist agent domains.
    Only domains with currently implemented and registered agents are active.
    """
    HR = "hr"
    IT = "it"
    KNOWLEDGE = "knowledge"
    # Note: Workflow and Analytics are included as per your architectural blueprint,
    # but the Coordinator will only route to them once their underlying modules exist.
    WORKFLOW = "workflow"
    ANALYTICS = "analytics"
    GENERAL = "general"
    UNKNOWN = "unknown"

# Allowed domains for quick lookups and validation during intent detection
SUPPORTED_DOMAINS: Final[FrozenSet[str]] = frozenset(
    domain.value for domain in AgentDomain if domain != AgentDomain.UNKNOWN
)

# =============================================================================
# EXECUTION & PLANNER STATUSES
# =============================================================================

class PlanStatus(str, Enum):
    """Statuses representing the state of a multi-step orchestration plan."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

# =============================================================================
# NETWORK & HEADERS
# =============================================================================

# Headers trusted for downstream service propagation.
# Existing codebase reference: Currently used in ai-service/src/api/router.py
TRUSTED_HEADERS: Final[FrozenSet[str]] = frozenset({
    "authorization",
    "x-tenant-id",
})

# =============================================================================
# SYSTEM DEFAULTS
# =============================================================================

# Maximum number of retry attempts for the Tool Executor when a specialist agent fails
MAX_TOOL_RETRIES: Final[int] = 3
