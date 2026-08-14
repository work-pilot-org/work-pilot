"""
Workflow Agent implementation.

The Workflow Agent receives natural-language workflow requests, uses the configured
LLM provider to decide which workflow tools are required, executes those tools,
and returns a final natural-language response.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from google.genai import types

from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.factory import get_llm_provider
from modules.workflow.tool_definitions import get_workflow_tool_definitions
from modules.workflow.tool_executor import (
    WorkflowToolExecutionError,
    WorkflowToolExecutor,
    workflow_tool_executor,
)

logger = get_logger(__name__)


WORKFLOW_SYSTEM_INSTRUCTION = """
You are the WorkPilot Workflow Agent.

You help users manage and interact with organizational workflows using the tools provided to you.

Rules:
- Use tools when information or an action requires the WorkPilot Workflow Service.
- Never invent workflow definitions, tasks, steps, executions, or tool results.
- Never claim an operation succeeded unless the corresponding tool succeeded.
- Use only the tools provided to you.
- If required information is missing, ask the user for it.
- Do not expose internal implementation details, tool names, API routes,
  stack traces, or service credentials.
- Base answers about WorkPilot Workflow data on tool results.
- Keep responses clear and concise.
"""


class WorkflowAgent:
    """
    AI agent responsible for workflow-related requests.
    """

    MAX_TOOL_ROUNDS = 5

    def __init__(
        self,
        provider: BaseLLMProvider | None = None,
        tool_executor: WorkflowToolExecutor | None = None,
    ) -> None:
        self._provider = provider or get_llm_provider()
        self._tool_executor = tool_executor or workflow_tool_executor
        self._tools = get_workflow_tool_definitions()

    async def run(
        self,
        message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> str:
        """
        Process a natural-language workflow request.
        """

        if not message.strip():
            raise ValueError("Workflow agent message cannot be empty.")

        logger.info("Workflow agent request started")

        contents: list[types.Content] = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=message),
                ],
            )
        ]

        for round_number in range(1, self.MAX_TOOL_ROUNDS + 1):
            logger.info(
                "Workflow agent LLM round",
                round_number=round_number,
            )

            response = await self._provider.generate_with_tools(
                contents,
                tools=self._tools,
                system_instruction=WORKFLOW_SYSTEM_INSTRUCTION,
            )

            candidate = self._get_candidate(response)

            # Preserve Gemini's response in conversation history.
            contents.append(candidate.content)

            function_calls = self._get_function_calls(candidate)

            # No function call means Gemini has produced the final answer.
            if not function_calls:
                final_text = self._extract_text(candidate)

                if not final_text:
                    logger.warning(
                        "Workflow agent received response without text or tool call"
                    )
                    return (
                        "I couldn't produce a response for that workflow request."
                    )

                logger.info("Workflow agent request completed")

                return final_text

            function_response_parts: list[types.Part] = []

            for function_call in function_calls:
                tool_name = function_call.name

                if not tool_name:
                    logger.warning(
                        "Gemini returned a function call without a name"
                    )
                    continue

                arguments = dict(function_call.args or {})

                logger.info(
                    "Workflow agent requested tool",
                    tool_name=tool_name,
                )

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

                except WorkflowToolExecutionError as exc:
                    logger.warning(
                        "Workflow tool execution returned an error",
                        tool_name=tool_name,
                        error=str(exc),
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
                    "Gemini requested tools but no valid responses were created"
                )
                return "I couldn't execute the requested workflow operation."

            # Function responses must be returned to Gemini so it can
            # interpret the tool results and continue the conversation.
            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        logger.warning(
            "Workflow agent exceeded maximum tool rounds",
            max_rounds=self.MAX_TOOL_ROUNDS,
        )

        return (
            "I couldn't complete the workflow request within the allowed "
            "number of operations."
        )

    @staticmethod
    def _get_candidate(response: Any) -> Any:
        candidates = getattr(response, "candidates", None)
        if not candidates:
            raise RuntimeError("Gemini returned no response candidates.")
        candidate = candidates[0]
        if candidate.content is None:
            raise RuntimeError("Gemini returned a candidate without content.")
        return candidate

    @staticmethod
    def _get_function_calls(candidate: Any) -> list[Any]:
        parts = candidate.content.parts or []
        return [
            part.function_call
            for part in parts
            if getattr(part, "function_call", None) is not None
        ]

    @staticmethod
    def _extract_text(candidate: Any) -> str:
        parts = candidate.content.parts or []
        text_parts = [
            part.text
            for part in parts
            if getattr(part, "text", None)
        ]
        return "".join(text_parts).strip()

    @staticmethod
    def _make_json_safe(value: Any) -> Any:
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")
        if isinstance(value, dict):
            return {
                str(key): WorkflowAgent._make_json_safe(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple, set)):
            return [
                WorkflowAgent._make_json_safe(item)
                for item in value
            ]
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)


@lru_cache
def get_workflow_agent() -> WorkflowAgent:
    """Return a lazily-initialized, cached WorkflowAgent instance."""
    return WorkflowAgent()
