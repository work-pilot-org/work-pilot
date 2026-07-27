"""
Coordinator Agent.

Routes user requests to the appropriate domain agent.
"""

from __future__ import annotations

from typing import Any

from core.logger import get_logger
from infrastructure.llm.gemini_client import gemini_client

from modules.hr.agent import get_hr_agent
from modules.it.agent import get_it_agent
# from modules.workflow.agent import get_workflow_agent
# from modules.analytics.agent import get_analytics_agent

logger = get_logger(__name__)


class CoordinatorAgent:
    """
    Main AI orchestrator.

    Responsibilities:
    - Receive the user's message.
    - Ask Gemini which domain should handle it.
    - Forward the request to the selected agent.
    """

    def __init__(self) -> None:
        self._agents = {
            "hr": get_hr_agent(),
            "it": get_it_agent(),
            # "workflow": get_workflow_agent(),
            # "analytics": get_analytics_agent(),
        }

    async def process(
        self,
        user_message: str,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Route the user request to the correct domain agent.
        """

        logger.info(
            "Processing user request",
            message=user_message,
        )

        # Gemini should return: hr / it / workflow / analytics
        tool_name = (
            await gemini_client.generate(user_message)
        ).strip().lower()

        logger.info(
            "Gemini selected agent",
            agent=tool_name,
        )

        agent = self._agents.get(tool_name)

        if agent is None:
            logger.warning(
                "Unknown agent selected",
                agent=tool_name,
            )

            return {
                "success": False,
                "message": (
                    f"Unknown agent '{tool_name}'. "
                    "Supported agents are: "
                    f"{', '.join(self._agents.keys())}."
                ),
            }

        return await agent.run(
            message=user_message,
            headers=headers,
        )


coordinator_agent = CoordinatorAgent()