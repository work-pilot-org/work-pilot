"""
AI Service API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from modules.coordinator.agent import CoordinatorAgent
from shared_infrastructure.core.security import get_current_user

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
    user: dict = Depends(get_current_user),
    coordinator: CoordinatorAgent = Depends(get_coordinator),
):
    headers = _extract_trusted_headers(request)

    trusted_tenant_id = user.get("tenant_id")
    if not trusted_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant ID is missing from credentials."
        )

    headers["x-tenant-id"] = str(trusted_tenant_id)

    result = await coordinator.process(
        user_message=body.message,
        headers=headers,
    )

    return {
        "success": True,
        "data": result,
    }