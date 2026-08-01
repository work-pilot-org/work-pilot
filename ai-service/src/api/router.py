"""
AI Service API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from modules.coordinator.agent import CoordinatorAgent
from modules.it.agent import ITAgent, get_it_agent

from .dependencies import get_coordinator

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class ChatRequest(BaseModel):
    message: str


# ==========================================================
# Headers trusted for downstream service propagation.
#
# Only these headers are forwarded from the incoming
# authenticated request to the IT Service.  The LLM
# never generates or controls them.
# ==========================================================

_TRUSTED_HEADERS = frozenset({
    "authorization",
    "x-tenant-id",
})


def _extract_trusted_headers(request: Request) -> dict[str, str]:
    """
    Extract only the trusted authentication/tenant headers
    from an incoming request.
    """
    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() in _TRUSTED_HEADERS
    }


@router.post("/chat")
async def chat(
    body: ChatRequest,
    request: Request,
    coordinator: CoordinatorAgent = Depends(get_coordinator),
):
    """
    Process an AI request.
    """

    headers = {
        key: value
        for key, value in request.headers.items()
    }

    result = await coordinator.process(
        user_message=body.message,
        headers=headers,
    )

    return {
        "success": True,
        "data": result,
    }


# ==========================================================
# IT Agent Endpoint
# ==========================================================

def _get_it_agent_dependency() -> ITAgent:
    """FastAPI dependency that returns the cached IT Agent."""
    return get_it_agent()


@router.post("/agents/it/chat")
async def it_agent_chat(
    body: ChatRequest,
    request: Request,
    agent: ITAgent = Depends(_get_it_agent_dependency),
):
    """
    Process an IT-specific AI request.

    The IT Agent uses the LLM to determine which IT tools
    to execute and returns a natural-language response.
    """

    headers = _extract_trusted_headers(request)

    result = await agent.run(
        message=body.message,
        headers=headers,
    )

    return {
        "response": result,
    }