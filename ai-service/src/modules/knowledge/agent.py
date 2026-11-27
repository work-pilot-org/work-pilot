"""
Knowledge Agent implementation.

The Knowledge Agent receives natural-language knowledge questions,
uses the configured LLM provider to decide when knowledge retrieval
is required, executes the selected knowledge tools, and returns a
grounded natural-language response.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from google.genai import types

from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.factory import get_llm_provider
from modules.knowledge.tool_definitions import (
    get_knowledge_tool_definitions,
)
from modules.knowledge.tool_executor import (
    KnowledgeToolExecutionError,
    KnowledgeToolExecutor,
)
from modules.knowledge.rag.retriever import KnowledgeRetriever


logger = get_logger(__name__)


KNOWLEDGE_SYSTEM_INSTRUCTION = """
You are the WorkPilot Knowledge Agent.

You answer questions using the organization's knowledge base.

Rules:

- Use the knowledge tools when the user's question requires
  information from the organization's knowledge base.
- Never invent company policies, procedures, facts, or documents.
- Base knowledge-base answers only on information returned by
  the knowledge tools.
- Never invent document IDs, tenant IDs, sources, or tool results.
- The tenant context is controlled by WorkPilot and must never be
  requested from or supplied by the user.
- Use only the tools provided to you.
- If the knowledge base does not contain enough information,
  clearly say that the information could not be found.
- Do not expose internal implementation details, tool names,
  API routes, embeddings, vector databases, stack traces,
  or service credentials.
- Keep responses clear, concise, and useful.
"""


class KnowledgeAgent:
    """
    AI agent responsible for organization knowledge questions.
    """

    MAX_TOOL_ROUNDS = 5

    def __init__(
        self,
        *,
        provider: BaseLLMProvider | None = None,
        tool_executor: KnowledgeToolExecutor,
    ) -> None:
        self._provider = provider or get_llm_provider()
        self._tool_executor = tool_executor
        self._tools = get_knowledge_tool_definitions()

    async def run(
        self,
        message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> str:
        """
        Process a natural-language knowledge request.

        Flow:

            user question
                ->
            Gemini
                ->
            optional knowledge tool call
                ->
            KnowledgeToolExecutor
                ->
            KnowledgeRetriever
                ->
            vector store
                ->
            tool result
                ->
            Gemini
                ->
            final grounded response
        """

        if not message.strip():
            raise ValueError(
                "Knowledge agent message cannot be empty."
            )

        headers = headers or {}
        tenant_id = headers.get("x-tenant-id", "").strip()

        if not tenant_id:
            raise ValueError(
                "Tenant ID is required for Knowledge Agent."
            )

        logger.info(
            "Knowledge agent request started",
            tenant_id=tenant_id,
        )

        contents: list[types.Content] = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message,
                    ),
                ],
            )
        ]

        for round_number in range(
            1,
            self.MAX_TOOL_ROUNDS + 1,
        ):
            logger.info(
                "Knowledge agent LLM round",
                round_number=round_number,
                tenant_id=tenant_id,
            )

            response = await self._provider.generate_with_tools(
                contents,
                tools=self._tools,
                system_instruction=KNOWLEDGE_SYSTEM_INSTRUCTION,
            )

            candidate = self._get_candidate(response)

            # Preserve Gemini's response in conversation history.
            contents.append(candidate.content)

            function_calls = self._get_function_calls(
                candidate
            )

            # No function call means Gemini has produced
            # the final answer.
            if not function_calls:
                final_text = self._extract_text(candidate)

                if not final_text:
                    logger.warning(
                        "Knowledge agent received response "
                        "without text or tool call",
                        tenant_id=tenant_id,
                    )

                    return (
                        "I couldn't produce a response "
                        "for that knowledge request."
                    )

                logger.info(
                    "Knowledge agent request completed",
                    tenant_id=tenant_id,
                )

                return final_text

            function_response_parts: list[types.Part] = []

            for function_call in function_calls:
                tool_name = function_call.name

                if not tool_name:
                    logger.warning(
                        "Gemini returned a knowledge function "
                        "call without a name"
                    )
                    continue

                arguments = dict(
                    function_call.args or {}
                )

                logger.info(
                    "Knowledge agent requested tool",
                    tool_name=tool_name,
                    tenant_id=tenant_id,
                )

                try:
                    result = await self._tool_executor.execute(
                        tool_name=tool_name,
                        arguments=arguments,
                        tenant_id=tenant_id,
                    )

                    tool_result = self._make_json_safe(
                        result
                    )

                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "success": True,
                                "result": tool_result,
                            },
                        )
                    )

                except KnowledgeToolExecutionError as exc:
                    logger.warning(
                        "Knowledge tool execution returned "
                        "an error",
                        tool_name=tool_name,
                        error=str(exc),
                        tenant_id=tenant_id,
                    )

                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "success": False,
                                "error": str(exc),
                            },
                        )
                    )

            if not function_response_parts:
                logger.error(
                    "Gemini requested knowledge tools but "
                    "no valid responses were created",
                    tenant_id=tenant_id,
                )

                return (
                    "I couldn't execute the requested "
                    "knowledge operation."
                )

            # Send tool results back to Gemini so it can
            # interpret the retrieved knowledge and generate
            # the final answer.
            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        logger.warning(
            "Knowledge agent exceeded maximum tool rounds",
            max_rounds=self.MAX_TOOL_ROUNDS,
            tenant_id=tenant_id,
        )

        return (
            "I couldn't complete the knowledge request "
            "within the allowed number of operations."
        )

    @staticmethod
    def _get_candidate(
        response: Any,
    ) -> Any:
        """
        Return the first Gemini response candidate.
        """

        candidates = getattr(
            response,
            "candidates",
            None,
        )

        if not candidates:
            raise RuntimeError(
                "Gemini returned no response candidates."
            )

        candidate = candidates[0]

        if candidate.content is None:
            raise RuntimeError(
                "Gemini returned a candidate without content."
            )

        return candidate

    @staticmethod
    def _get_function_calls(
        candidate: Any,
    ) -> list[Any]:
        """
        Extract function calls from all response parts.
        """

        parts = candidate.content.parts or []

        return [
            part.function_call
            for part in parts
            if getattr(
                part,
                "function_call",
                None,
            ) is not None
        ]

    @staticmethod
    def _extract_text(
        candidate: Any,
    ) -> str:
        """
        Extract textual content from a Gemini candidate.
        """

        parts = candidate.content.parts or []

        text_parts = [
            part.text
            for part in parts
            if getattr(
                part,
                "text",
                None,
            )
        ]

        return "".join(text_parts).strip()

    @staticmethod
    def _make_json_safe(
        value: Any,
    ) -> Any:
        """
        Convert tool results into values suitable for a
        Gemini function response.
        """

        if value is None:
            return None

        if hasattr(value, "model_dump"):
            return value.model_dump(
                mode="json"
            )

        if isinstance(value, dict):
            return {
                str(key): KnowledgeAgent._make_json_safe(
                    item
                )
                for key, item in value.items()
            }

        if isinstance(
            value,
            (list, tuple, set),
        ):
            return [
                KnowledgeAgent._make_json_safe(
                    item
                )
                for item in value
            ]

        if isinstance(
            value,
            (str, int, float, bool),
        ):
            return value

        return str(value)


def create_knowledge_agent(
    *,
    retriever: KnowledgeRetriever,
    provider: BaseLLMProvider | None = None,
) -> KnowledgeAgent:
    """
    Create a KnowledgeAgent with the supplied retriever.

    The retriever is injected into the KnowledgeToolExecutor.
    """

    tool_executor = KnowledgeToolExecutor(
        retriever=retriever,
    )

    return KnowledgeAgent(
        provider=provider,
        tool_executor=tool_executor,
    )


@lru_cache
def get_knowledge_agent() -> KnowledgeAgent:
    """
    Return a lazily-initialized, cached KnowledgeAgent instance.
    """
    from modules.knowledge.rag.providers.google_embeddings import GeminiEmbeddingProvider
    from modules.knowledge.rag.providers.chroma import ChromaVectorStore

    embedding_provider = GeminiEmbeddingProvider()
    vector_store = ChromaVectorStore()
    retriever = KnowledgeRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    return create_knowledge_agent(
        retriever=retriever,
    )