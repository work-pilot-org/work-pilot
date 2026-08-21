"""
Analytics Agent implementation.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from google.genai import types

from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.factory import get_llm_provider

from modules.analytics.tool_definitions import get_analytics_tool_definitions
from modules.analytics.tool_executor import (
    AnalyticsToolExecutionError,
    AnalyticsToolExecutor,
    analytics_tool_executor,
)
from modules.analytics.prompts import ANALYTICS_SYSTEM_INSTRUCTION

logger = get_logger(__name__)


class AnalyticsAgent:
    MAX_TOOL_ROUNDS = 5

    def __init__(
        self,
        provider: BaseLLMProvider | None = None,
        tool_executor: AnalyticsToolExecutor | None = None,
    ) -> None:
        self._provider = provider or get_llm_provider()
        self._tool_executor = tool_executor or analytics_tool_executor
        self._tools = get_analytics_tool_definitions()

    async def run(
        self,
        message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> str:
        if not message.strip():
            raise ValueError("Analytics agent message cannot be empty.")

        logger.info("Analytics agent request started")

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)],
            )
        ]

        for round_number in range(1, self.MAX_TOOL_ROUNDS + 1):
            logger.info("Analytics agent LLM round", round_number=round_number)

            response = await self._provider.generate_with_tools(
                contents,
                tools=self._tools,
                system_instruction=ANALYTICS_SYSTEM_INSTRUCTION,
            )

            candidate = self._get_candidate(response)
            contents.append(candidate.content)

            function_calls = self._get_function_calls(candidate)

            if not function_calls:
                final_text = self._extract_text(candidate)
                if not final_text:
                    logger.warning("Analytics agent received response without text or tool call")
                    return "I couldn't produce a response for that Analytics request."
                logger.info("Analytics agent request completed")
                return final_text

            function_response_parts = []
            for function_call in function_calls:
                tool_name = function_call.name
                if not tool_name:
                    logger.warning("Gemini returned a function call without a name")
                    continue

                arguments = dict(function_call.args or {})
                logger.info("Analytics agent requested tool", tool_name=tool_name)

                try:
                    result = await self._tool_executor.execute(
                        tool_name=tool_name,
                        arguments=arguments,
                        headers=headers,
                    )
                    tool_result = self._make_json_safe(result)
                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "success": True,
                                "result": tool_result,
                            },
                        )
                    )
                except AnalyticsToolExecutionError as exc:
                    logger.warning("Analytics tool execution failed", tool_name=tool_name, error=str(exc))
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
                logger.error("Gemini requested tools but no responses were generated")
                return "I couldn't execute the requested Analytics operation."

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        logger.warning("Analytics agent exceeded maximum tool rounds", max_rounds=self.MAX_TOOL_ROUNDS)
        return "I couldn't complete the Analytics request within the allowed number of operations."

    @staticmethod
    def _get_candidate(response: Any):
        candidates = getattr(response, "candidates", None)
        if not candidates:
            raise RuntimeError("Gemini returned no response candidates.")
        candidate = candidates[0]
        if candidate.content is None:
            raise RuntimeError("Gemini returned a candidate without content.")
        return candidate

    @staticmethod
    def _get_function_calls(candidate: Any):
        parts = candidate.content.parts or []
        return [
            part.function_call
            for part in parts
            if getattr(part, "function_call", None) is not None
        ]

    @staticmethod
    def _extract_text(candidate: Any):
        parts = candidate.content.parts or []
        text_parts = [part.text for part in parts if getattr(part, "text", None)]
        return "".join(text_parts).strip()

    @staticmethod
    def _make_json_safe(value: Any):
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")
        if isinstance(value, dict):
            return {str(key): AnalyticsAgent._make_json_safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [AnalyticsAgent._make_json_safe(item) for item in value]
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)


@lru_cache
def get_analytics_agent() -> AnalyticsAgent:
    return AnalyticsAgent()
