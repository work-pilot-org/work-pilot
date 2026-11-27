"""
Tests for the Knowledge Agent and its related coordinator, tool execution,
and security flows.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
import pytest
from google.genai import types
from fastapi import HTTPException

# Modules under test
from modules.knowledge.agent import KnowledgeAgent, get_knowledge_agent
from modules.knowledge.tool_definitions import get_knowledge_tool_definitions
from modules.knowledge.tool_executor import KnowledgeToolExecutionError, KnowledgeToolExecutor
from modules.knowledge.registry import tool_registry
from modules.knowledge.rag.retriever import KnowledgeRetriever
from modules.knowledge.schemas import RetrievedDocument
from modules.coordinator.constants import AgentDomain
from modules.coordinator.registry import agent_registry
from modules.coordinator.agent import CoordinatorAgent
from api.router import chat, ChatRequest

from infrastructure.providers.base_provider import BaseLLMProvider


# ==========================================================
# Fakes and Mocks
# ==========================================================

class FakeGeminiResponse:
    def __init__(self, content: types.Content) -> None:
        self.candidates = [FakeCandidate(content)]


class FakeCandidate:
    def __init__(self, content: types.Content) -> None:
        self.content = content


class FakeLLMProvider(BaseLLMProvider):
    """
    Fake LLM provider that simulates a search_documents tool call,
    followed by a final grounded response.
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
            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_function_call(
                        name="search_documents",
                        args={"query": "leave policy", "top_k": 5},
                    )
                ],
            )
            return FakeGeminiResponse(content)

        content = types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="Employees receive 20 days of annual leave per year."
                )
            ],
        )
        return FakeGeminiResponse(content)


class FakeRetriever:
    def __init__(self) -> None:
        self.last_query = None
        self.last_top_k = None
        self.last_tenant_id = None

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int,
        tenant_id: str,
    ) -> list[RetrievedDocument]:
        self.last_query = query
        self.last_top_k = top_k
        self.last_tenant_id = tenant_id
        return [
            RetrievedDocument(
                document_id="doc-1",
                content="Employees receive 20 days of annual leave per year.",
                score=0.95,
                source="leave_policy.pdf",
                metadata={"tenant_id": tenant_id}
            )
        ]


# ==========================================================
# 1. KNOWLEDGE AGENT TESTS
# ==========================================================

@pytest.mark.asyncio
async def test_knowledge_agent_valid_request():
    fake_retriever = FakeRetriever()
    tool_executor = KnowledgeToolExecutor(retriever=fake_retriever)
    agent = KnowledgeAgent(
        provider=FakeLLMProvider(),
        tool_executor=tool_executor,
    )

    response = await agent.run(
        message="How many days of annual leave do employees receive?",
        headers={"x-tenant-id": "tenant-a"},
    )

    assert "20 days" in response
    assert fake_retriever.last_tenant_id == "tenant-a"
    assert fake_retriever.last_query == "leave policy"


@pytest.mark.asyncio
async def test_knowledge_agent_missing_headers():
    fake_retriever = FakeRetriever()
    tool_executor = KnowledgeToolExecutor(retriever=fake_retriever)
    agent = KnowledgeAgent(
        provider=FakeLLMProvider(),
        tool_executor=tool_executor,
    )

    with pytest.raises(ValueError, match="Tenant ID is required"):
        await agent.run(
            message="How many days of annual leave do employees receive?",
            headers=None,
        )


@pytest.mark.asyncio
async def test_knowledge_agent_missing_x_tenant_id():
    fake_retriever = FakeRetriever()
    tool_executor = KnowledgeToolExecutor(retriever=fake_retriever)
    agent = KnowledgeAgent(
        provider=FakeLLMProvider(),
        tool_executor=tool_executor,
    )

    with pytest.raises(ValueError, match="Tenant ID is required"):
        await agent.run(
            message="How many days of annual leave do employees receive?",
            headers={},
        )


@pytest.mark.asyncio
async def test_knowledge_agent_empty_x_tenant_id():
    fake_retriever = FakeRetriever()
    tool_executor = KnowledgeToolExecutor(retriever=fake_retriever)
    agent = KnowledgeAgent(
        provider=FakeLLMProvider(),
        tool_executor=tool_executor,
    )

    with pytest.raises(ValueError, match="Tenant ID is required"):
        await agent.run(
            message="How many days of annual leave do employees receive?",
            headers={"x-tenant-id": " "},
        )


# ==========================================================
# 2. KNOWLEDGE TOOL EXECUTOR TESTS
# ==========================================================

@pytest.mark.asyncio
async def test_executor_search_documents_success():
    fake_retriever = FakeRetriever()
    executor = KnowledgeToolExecutor(retriever=fake_retriever)

    result = await executor.execute(
        tool_name="search_documents",
        arguments={"query": "leave policy", "top_k": 3},
        tenant_id="tenant-a",
    )

    assert len(result) == 1
    assert result[0].content == "Employees receive 20 days of annual leave per year."
    assert fake_retriever.last_query == "leave policy"
    assert fake_retriever.last_top_k == 3
    assert fake_retriever.last_tenant_id == "tenant-a"


@pytest.mark.asyncio
async def test_executor_tenant_id_injection_protection():
    fake_retriever = FakeRetriever()
    executor = KnowledgeToolExecutor(retriever=fake_retriever)

    with pytest.raises(KnowledgeToolExecutionError, match="Unexpected arguments for Knowledge tool: tenant_id"):
        await executor.execute(
            tool_name="search_documents",
            arguments={"query": "leave policy", "tenant_id": "attacker-tenant"},
            tenant_id="tenant-trusted",
        )


@pytest.mark.asyncio
async def test_executor_rejects_unknown_tool():
    fake_retriever = FakeRetriever()
    executor = KnowledgeToolExecutor(retriever=fake_retriever)

    with pytest.raises(KnowledgeToolExecutionError, match="Unknown Knowledge tool"):
        await executor.execute(
            tool_name="unknown_it_tool",
            arguments={"query": "hello"},
            tenant_id="tenant-a",
        )


@pytest.mark.asyncio
async def test_executor_rejects_missing_required_arguments():
    fake_retriever = FakeRetriever()
    executor = KnowledgeToolExecutor(retriever=fake_retriever)

    with pytest.raises(KnowledgeToolExecutionError, match="Missing required argument: query"):
        await executor.execute(
            tool_name="search_documents",
            arguments={"top_k": 5},
            tenant_id="tenant-a",
        )


@pytest.mark.asyncio
async def test_executor_rejects_unexpected_arguments():
    fake_retriever = FakeRetriever()
    executor = KnowledgeToolExecutor(retriever=fake_retriever)

    with pytest.raises(KnowledgeToolExecutionError, match="Unexpected arguments"):
        await executor.execute(
            tool_name="search_documents",
            arguments={"query": "test", "unexpected_arg": "value"},
            tenant_id="tenant-a",
        )


# ==========================================================
# 3. TOOL DEFINITIONS TESTS
# ==========================================================

def test_tool_definitions_do_not_expose_internal_params():
    definitions = get_knowledge_tool_definitions()

    assert len(definitions) == 1

    function_declarations = definitions[0].function_declarations

    tool_names = {
        declaration.name
        for declaration in function_declarations
    }

    assert tool_names == {
        "search_documents",
        "search_faq",
        "search_policies",
        "get_system_capabilities",
    }

    # Internal application-controlled parameters must never
    # be exposed to the LLM as tool arguments.
    for declaration in function_declarations:
        parameters = declaration.parameters

        if parameters and parameters.properties:
            assert "tenant_id" not in parameters.properties
            assert "retriever" not in parameters.properties# ==========================================================
# 4. REGISTRY TESTS
# ==========================================================

def test_registry_contains_knowledge_agent():
    assert AgentDomain.KNOWLEDGE.value == "knowledge"
    
    agent = agent_registry.get_agent("knowledge")
    assert isinstance(agent, KnowledgeAgent)

    # Verify existing agents still resolve
    assert agent_registry.get_agent("it")
    assert agent_registry.get_agent("hr")


# ==========================================================
# 5. COORDINATOR INTEGRATION & INTENT ROUTING
# ==========================================================

class FakeIntentDetector:
    async def detect_intent(self, user_message: str):
        from modules.coordinator.intent_detector import IntentClassification
        return IntentClassification(domain="knowledge", intent="SEARCH_DOCUMENTS")


class FakePlanner:
    async def generate_plan(self, user_message: str, intent_classification: Any):
        from modules.coordinator.planner import ExecutionPlan, PlanStep
        return ExecutionPlan(
            plan=[PlanStep(step_number=1, description="Search documentation for policy details")]
        )


@pytest.mark.asyncio
async def test_coordinator_routes_to_knowledge_agent(monkeypatch):
    coordinator = CoordinatorAgent()

    # Stub the intent detector and planner to avoid calling Gemini APIs
    monkeypatch.setattr("modules.coordinator.agent.intent_detector", FakeIntentDetector())
    monkeypatch.setattr("modules.coordinator.agent.orchestration_planner", FakePlanner())

    # Stub the agent registry to return a mock SpecialistAgent
    class MockSpecialistAgent:
        async def run(self, message: str, *, headers: dict[str, str] | None = None) -> str:
            return "Employees receive 20 days of annual leave per year."

    monkeypatch.setattr(
        agent_registry, 
        "get_agent", 
        lambda domain: MockSpecialistAgent() if domain == "knowledge" else None
    )

    result = await coordinator.process(
        user_message="How many days of annual leave do employees receive?",
        headers={"x-tenant-id": "tenant-a"},
    )

    # Coordinator process returns a text summary or a fallback string.
    # In success cases, it will build success response or fallback raw results.
    assert "20 days" in result


# ==========================================================
# 6. TENANT HEADER OVERRIDE TESTS
# ==========================================================

class MockRequest:
    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = headers


@pytest.mark.asyncio
async def test_router_overwrites_client_x_tenant_id(monkeypatch):
    # Simulated coordinator agent
    class MockCoordinator:
        def __init__(self) -> None:
            self.last_headers = None

        async def process(self, user_message: str, headers: dict[str, str] | None = None):
            self.last_headers = headers
            return "Grounded result"

    mock_coordinator = MockCoordinator()
    
    # Mock JWT user representation
    mock_user = {"tenant_id": "tenant-trusted-jwt-a"}
    mock_request = MockRequest({
        "authorization": "Bearer token",
        "x-tenant-id": "tenant-attacker-b"
    })

    # Call the chat route directly
    result = await chat(
        body=ChatRequest(message="What is the leave policy?"),
        request=mock_request,
        user=mock_user,
        coordinator=mock_coordinator,
    )

    assert result["success"] is True
    # The attacker's header must be completely overwritten by the JWT's tenant_id value
    assert mock_coordinator.last_headers.get("x-tenant-id") == "tenant-trusted-jwt-a"


@pytest.mark.asyncio
async def test_router_fails_on_missing_jwt_tenant_id(monkeypatch):
    mock_coordinator = MagicMock()
    mock_user = {}  # Missing tenant_id field
    mock_request = MockRequest({
        "authorization": "Bearer token",
        "x-tenant-id": "tenant-attacker-b"
    })

    with pytest.raises(HTTPException) as exc:
        await chat(
            body=ChatRequest(message="What is the leave policy?"),
            request=mock_request,
            user=mock_user,
            coordinator=mock_coordinator,
        )

    assert exc.value.status_code == 401
    assert "Tenant ID is missing" in exc.value.detail


# ==========================================================
# 7. RAG ISOLATION & RETRIEVER TESTS
# ==========================================================

@pytest.mark.asyncio
async def test_retriever_forwards_trusted_tenant_to_vector_store():
    class FakeVectorStore:
        def __init__(self) -> None:
            self.last_tenant_id = None

        async def search(self, query_embedding: list[float], top_k: int, tenant_id: str):
            self.last_tenant_id = tenant_id
            return [{
                "document_id": "doc-abc",
                "content": "Policy contents",
                "score": 0.85,
                "source": "leave.pdf"
            }]

    class FakeEmbeddingProvider:
        async def embed_text(self, text: str) -> list[float]:
            return [0.1] * 3072

    vector_store = FakeVectorStore()
    embedding_provider = FakeEmbeddingProvider()
    
    retriever = KnowledgeRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    results = await retriever.retrieve(
        query="What is the leave policy?",
        top_k=5,
        tenant_id="tenant-isolated-123"
    )

    assert len(results) == 1
    assert results[0].document_id == "doc-abc"
    assert vector_store.last_tenant_id == "tenant-isolated-123"


# ==========================================================
# 8. GET_SYSTEM_CAPABILITIES TESTS
# ==========================================================

@pytest.mark.asyncio
async def test_get_system_capabilities_tool():
    from modules.knowledge.tools.get_system_capabilities import get_system_capabilities
    
    result = await get_system_capabilities()
    assert "domains" in result
    assert "hr" in result["domains"]
    assert "it" in result["domains"]
    assert "knowledge" in result["domains"]
    
    # Assert counts match registries
    from modules.hr.registry import hr_tool_registry
    from modules.it.registry import tool_registry as it_tool_registry
    from modules.knowledge.registry import tool_registry as knowledge_tool_registry
    
    assert result["domains"]["hr"]["tools_count"] == len(hr_tool_registry.list_tools())
    assert result["domains"]["it"]["tools_count"] == len(it_tool_registry.list_tools())
    assert result["domains"]["knowledge"]["tools_count"] == len(knowledge_tool_registry.list_tools())


@pytest.mark.asyncio
async def test_knowledge_agent_calls_get_system_capabilities():
    class FakeCapabilitiesLLMProvider(BaseLLMProvider):
        def __init__(self) -> None:
            self.call_count = 0
            
        async def generate(self, prompt: str, *, system_instruction: str | None = None) -> str:
            return "Fake response"
            
        async def generate_with_tools(self, contents: Any, *, tools: list[Any], system_instruction: str | None = None) -> Any:
            self.call_count += 1
            if self.call_count == 1:
                content = types.Content(
                    role="model",
                    parts=[
                        types.Part.from_function_call(
                            name="get_system_capabilities",
                            args={},
                        )
                    ],
                )
                return FakeGeminiResponse(content)
            
            content = types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="Here are the capabilities: HR has employee management, IT has ticket support."
                    )
                ],
            )
            return FakeGeminiResponse(content)

    fake_retriever = FakeRetriever()
    tool_executor = KnowledgeToolExecutor(retriever=fake_retriever)
    agent = KnowledgeAgent(
        provider=FakeCapabilitiesLLMProvider(),
        tool_executor=tool_executor,
    )
    
    response = await agent.run(
        message="What can you help me with?",
        headers={"x-tenant-id": "tenant-test"}
    )
    assert "capabilities" in response.lower()

