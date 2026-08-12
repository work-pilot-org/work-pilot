"""
AI Service API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel

from modules.coordinator.agent import CoordinatorAgent
from shared_infrastructure.core.security import get_current_user
from infrastructure.providers.exceptions import GeminiRateLimitError, GeminiQuotaExhaustedError

from .dependencies import get_coordinator

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(get_current_user)],
)


class ChatRequest(BaseModel):
    message: str


_TRUSTED_HEADERS = frozenset({
    "authorization",
    "x-tenant-id",
})


def _extract_trusted_headers(request: Request) -> dict[str, str]:
    """
    Extract only trusted authentication headers that should be
    forwarded to downstream services.
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
    current_user: dict = Depends(get_current_user),
):
    # Extract authorization header to pass down to internal services
    auth_header = request.headers.get("authorization")
    
    # Securely derive tenant_id from the verified JWT token payload
    # rather than trusting an arbitrary x-tenant-id header.
    tenant_id = str(current_user.get("tenant_id")) if current_user.get("tenant_id") else None

    headers = {}
    if auth_header:
        headers["authorization"] = auth_header
    if tenant_id:
        headers["x-tenant-id"] = tenant_id

    try:
        result = await coordinator.process(
            user_message=body.message,
            headers=headers,
            user_context=current_user,
        )

        return {
            "success": True,
            "data": result,
        }
    except (GeminiRateLimitError, GeminiQuotaExhaustedError):
        raise HTTPException(status_code=429, detail="AI Service quota temporarily unavailable. Please try again later.")
    except Exception as e:
        # Assuming the CoordinatorAgent raised a CoordinatorError with a nice message
        raise HTTPException(status_code=500, detail=str(e))