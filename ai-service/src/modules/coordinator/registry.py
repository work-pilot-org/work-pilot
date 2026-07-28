# Agent registry
"""
Agent Registry for the Coordinator.

This module maps domain strings to their respective specialist agent instances.
It acts as the single source of truth for available downstream agents,
preventing hardcoded imports from scattering across the orchestration layer.
"""

from typing import Any, Dict, Protocol

from modules.coordinator.constants import AgentDomain
from modules.coordinator.exceptions import UnknownDomainError

# Strict reuse of your existing agent factory functions
from modules.hr.agent import get_hr_agent
from modules.it.agent import get_it_agent


class SpecialistAgent(Protocol):
    """
    Interface definition for all specialist agents.
    This ensures the Coordinator can interact with any agent uniformly 
    without knowing its internal business logic (SOLID).
    """
    async def run(
        self, 
        message: str, 
        *, 
        headers: dict[str, str] | None = None
    ) -> Any:
        ...


class AgentRegistry:
    """
    Maintains the mapping of domains to specialist agent instances.
    """

    def __init__(self) -> None:
        # We eagerly initialize the registry using your existing factories.
        # Workflow and Analytics are intentionally omitted here until 
        # their underlying agents are actually implemented in the codebase.
        self._agents: Dict[str, SpecialistAgent] = {
            AgentDomain.HR.value: get_hr_agent(),
            AgentDomain.IT.value: get_it_agent(),
        }

    def get_agent(self, domain: str) -> SpecialistAgent:
        """
        Retrieves the specialist agent instance for a given domain.
        
        Args:
            domain (str): The domain string (e.g., 'hr', 'it').
            
        Raises:
            UnknownDomainError: If the requested domain is not registered.
        """
        agent = self._agents.get(domain)
        if not agent:
            raise UnknownDomainError(domain)
            
        return agent


# Singleton instance for the coordinator module
agent_registry = AgentRegistry()
