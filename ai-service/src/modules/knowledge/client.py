"""
Knowledge Agent client.

Handles final answer generation using retrieved
knowledge-base context.
"""

from __future__ import annotations

from core.logger import get_logger
from infrastructure.llm.gemini_client import gemini_client

from modules.knowledge.prompts import (
    build_knowledge_answer_prompt,
)

logger = get_logger(__name__)


class KnowledgeClient:
    """
    Handles LLM interactions for the Knowledge Agent.
    """

    async def generate_answer(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate an answer using retrieved knowledge.
        """

        prompt = build_knowledge_answer_prompt(
            user_query=query,
            context=context,
        )

        logger.info(
            "Generating knowledge response",
            query=query,
        )

        response = await gemini_client.generate(
            prompt=prompt,
        )

        return response.strip()


knowledge_client = KnowledgeClient()