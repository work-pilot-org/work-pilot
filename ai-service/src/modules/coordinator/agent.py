"""
Coordinator Agent.

Routes user requests to the appropriate domain agent.
"""

from __future__ import annotations

from typing import Any

from core.logger import get_logger
from infrastructure.llm.gemini_client import gemini_client
from modules.it.agent import get_it_agent

logger = get_logger(__name__)


class CoordinatorAgent:
    """
    Main orchestrator of the AI Service.
    """

    async def process(
        self,
        user_message: str,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Process a user's request.
        """

        logger.info(
            "Processing user request",
            message=user_message,
        )

        # Ask Gemini to determine which tool should be used.
        tool_name = await gemini_client.generate(user_message)

        tool_name = tool_name.strip()

        logger.info(
            "Gemini selected tool",
            tool_name=tool_name,
        )

        # Temporary implementation:
        # Route everything to the IT Agent.
        return await get_it_agent().execute(
            tool_name=tool_name,
            headers=headers,
        )


coordinator_agent = CoordinatorAgent()