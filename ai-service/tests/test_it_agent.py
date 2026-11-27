from __future__ import annotations

from typing import Any

import pytest
from google.genai import types

from infrastructure.providers.base_provider import BaseLLMProvider
from modules.it.agent import ITAgent
from modules.it.tool_executor import ITToolExecutionError


class FakeLLMProvider(BaseLLMProvider):
    """
    Fake LLM provider.

    First call requests list_devices.
    Second call returns the final answer.
    """

    def __init__(self) -> None:
        self.call_count = 0
        self.received_contents: list[Any] = []

    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
    ) -> str:
        return "Fake response"

    async def generate_with_tools(
        self,
        contents: Any,
        *,
        tools: list[Any],
        system_instruction: str | None = None,
    ) -> Any:
        self.call_count += 1
        self.received_contents.append(contents)

        if self.call_count == 1:
            return self._tool_call_response()

        return self._final_response()

    @staticmethod
    def _tool_call_response() -> Any:
        content = types.Content(
            role="model",
            parts=[
                types.Part.from_function_call(
                    name="list_devices",
                    args={},
                )
            ],
        )

        return FakeGeminiResponse(content)

    @staticmethod
    def _final_response() -> Any:
        content = types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="You have a Dell Latitude device."
                )
            ],
        )

        return FakeGeminiResponse(content)


class FakeCandidate:
    def __init__(self, content: types.Content) -> None:
        self.content = content


class FakeGeminiResponse:
    def __init__(self, content: types.Content) -> None:
        self.candidates = [
            FakeCandidate(content)
        ]


class FakeToolExecutor:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        headers: dict[str, str] | None = None,
    ) -> Any:
        self.calls.append(
            {
                "tool_name": tool_name,
                "arguments": arguments,
                "headers": headers,
            }
        )

        if tool_name == "list_devices":
            return [
                {
                    "name": "Dell Latitude",
                    "status": "ACTIVE",
                }
            ]

        if tool_name == "get_device":
            return {
                "id": arguments.get("device_id"),
                "name": "Dell Latitude",
                "status": "ACTIVE",
            }

        if tool_name == "list_assets":
            return [
                {"name": "Monitor", "status": "AVAILABLE"},
            ]

        raise RuntimeError(
            f"Unexpected tool: {tool_name}"
        )


# ==========================================================
# Test 1: LLM requests one tool -> executor -> final answer
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_executes_tool_and_returns_final_answer():
    provider = FakeLLMProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    headers = {
        "Authorization": "Bearer test-token",
        "X-Tenant-ID": "tenant-123",
    }

    result = await agent.run(
        "Show me my devices",
        headers=headers,
    )

    assert result == "You have a Dell Latitude device."

    # First LLM call asks for a tool.
    # Second LLM call interprets its result.
    assert provider.call_count == 2

    assert len(executor.calls) == 1

    call = executor.calls[0]

    assert call["tool_name"] == "list_devices"
    assert call["arguments"] == {}
    assert call["headers"] == headers


# ==========================================================
# Test 2: Direct LLM response (no tool call)
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_returns_direct_llm_answer():
    class DirectProvider(FakeLLMProvider):
        async def generate_with_tools(
            self,
            contents: Any,
            *,
            tools: list[Any],
            system_instruction: str | None = None,
        ) -> Any:
            self.call_count += 1

            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="How can I help with your IT request?"
                    )
                ],
            )

            return FakeGeminiResponse(content)

    provider = DirectProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    result = await agent.run("Hello")

    assert result == "How can I help with your IT request?"
    assert provider.call_count == 1
    assert executor.calls == []


# ==========================================================
# Test 3: Headers are propagated to the executor
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_propagates_headers_to_executor():
    provider = FakeLLMProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    headers = {
        "Authorization": "Bearer secret-jwt",
        "X-Tenant-ID": "org-456",
    }

    await agent.run(
        "List devices",
        headers=headers,
    )

    assert len(executor.calls) == 1
    assert executor.calls[0]["headers"] is headers
    assert executor.calls[0]["headers"]["Authorization"] == "Bearer secret-jwt"
    assert executor.calls[0]["headers"]["X-Tenant-ID"] == "org-456"


# ==========================================================
# Test 4: Tool arguments are passed correctly
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_passes_tool_arguments():
    device_id = "550e8400-e29b-41d4-a716-446655440000"

    class ArgsProvider(FakeLLMProvider):
        async def generate_with_tools(
            self,
            contents: Any,
            *,
            tools: list[Any],
            system_instruction: str | None = None,
        ) -> Any:
            self.call_count += 1
            self.received_contents.append(contents)

            if self.call_count == 1:
                content = types.Content(
                    role="model",
                    parts=[
                        types.Part.from_function_call(
                            name="get_device",
                            args={"device_id": device_id},
                        )
                    ],
                )
                return FakeGeminiResponse(content)

            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="Here is your Dell Latitude."
                    )
                ],
            )
            return FakeGeminiResponse(content)

    provider = ArgsProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    result = await agent.run("Show device details")

    assert result == "Here is your Dell Latitude."
    assert len(executor.calls) == 1
    assert executor.calls[0]["tool_name"] == "get_device"
    assert executor.calls[0]["arguments"] == {"device_id": device_id}


# ==========================================================
# Test 5: Tool execution failure is handled cleanly
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_handles_tool_execution_error():
    class FailingExecutor:
        def __init__(self) -> None:
            self.calls: list[dict[str, Any]] = []

        async def execute(
            self,
            tool_name: str,
            arguments: dict[str, Any] | None = None,
            *,
            headers: dict[str, str] | None = None,
        ) -> Any:
            self.calls.append(
                {
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "headers": headers,
                }
            )

            raise ITToolExecutionError(
                "Device service unavailable"
            )

    class ErrorRecoveryProvider(FakeLLMProvider):
        async def generate_with_tools(
            self,
            contents: Any,
            *,
            tools: list[Any],
            system_instruction: str | None = None,
        ) -> Any:
            self.call_count += 1
            self.received_contents.append(contents)

            if self.call_count == 1:
                return self._tool_call_response()

            # After receiving a tool error, LLM produces text.
            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="Sorry, I could not retrieve devices."
                    )
                ],
            )
            return FakeGeminiResponse(content)

    provider = ErrorRecoveryProvider()
    executor = FailingExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    result = await agent.run("List devices")

    assert result == "Sorry, I could not retrieve devices."
    assert provider.call_count == 2
    assert len(executor.calls) == 1


# ==========================================================
# Test 6: Maximum tool-round protection
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_enforces_max_tool_rounds():
    class InfiniteToolProvider(FakeLLMProvider):
        """Always requests a tool call, never returns text."""

        async def generate_with_tools(
            self,
            contents: Any,
            *,
            tools: list[Any],
            system_instruction: str | None = None,
        ) -> Any:
            self.call_count += 1
            self.received_contents.append(contents)
            return self._tool_call_response()

    provider = InfiniteToolProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    result = await agent.run("List devices")

    # Agent should stop after MAX_TOOL_ROUNDS and return a safe message.
    assert "couldn't complete" in result.lower()
    assert provider.call_count == ITAgent.MAX_TOOL_ROUNDS
    assert len(executor.calls) == ITAgent.MAX_TOOL_ROUNDS


# ==========================================================
# Test 7: Multiple tool calls in a single LLM response
# ==========================================================

@pytest.mark.asyncio
async def test_it_agent_handles_multiple_tool_calls_in_one_response():
    class MultiToolProvider(FakeLLMProvider):
        async def generate_with_tools(
            self,
            contents: Any,
            *,
            tools: list[Any],
            system_instruction: str | None = None,
        ) -> Any:
            self.call_count += 1
            self.received_contents.append(contents)

            if self.call_count == 1:
                # Return two tool calls in one response.
                content = types.Content(
                    role="model",
                    parts=[
                        types.Part.from_function_call(
                            name="list_devices",
                            args={},
                        ),
                        types.Part.from_function_call(
                            name="list_assets",
                            args={},
                        ),
                    ],
                )
                return FakeGeminiResponse(content)

            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="You have 1 device and 1 asset."
                    )
                ],
            )
            return FakeGeminiResponse(content)

    provider = MultiToolProvider()
    executor = FakeToolExecutor()

    agent = ITAgent(
        provider=provider,
        tool_executor=executor,
    )

    result = await agent.run("Show me everything")

    assert result == "You have 1 device and 1 asset."
    assert provider.call_count == 2
    assert len(executor.calls) == 2
    assert executor.calls[0]["tool_name"] == "list_devices"
    assert executor.calls[1]["tool_name"] == "list_assets"