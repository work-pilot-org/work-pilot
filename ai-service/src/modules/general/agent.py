"""
General Agent implementation.

Handles general conversational intents, greetings, and chit-chat.
"""

from typing import Any

from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.factory import get_llm_provider

logger = get_logger(__name__)


GENERAL_SYSTEM_INSTRUCTION = """
You are WorkPilot AI, an intelligent, helpful, and polite enterprise assistant.
You are currently handling a general conversational request (like a greeting).
Be brief, professional, and welcoming. Do not make up any company information.
"""


class GeneralAgent:
    """
    AI agent responsible for general conversation.
    """

    def __init__(self, *, provider: BaseLLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()

    async def run(
        self,
        message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> str:
        """
        Process a natural-language general conversation request.
        """
        if not message.strip():
            return "Hello! How can I help you today?"

        logger.info("General agent request started")

        response = await self._provider.generate(
            prompt=message,
            system_instruction=GENERAL_SYSTEM_INSTRUCTION,
        )

        logger.info("General agent request completed")
        return response


def get_general_agent() -> GeneralAgent:
    """
    Return a new GeneralAgent instance.
    """
    return GeneralAgent()
