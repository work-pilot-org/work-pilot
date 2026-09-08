"""
AI Service API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from shared_infrastructure.database.session import get_db
from src.modules.conversation.service import ConversationService
from src.modules.conversation.schemas import ConversationResponse

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
    conversation_id: Optional[UUID] = None


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
    db: Session = Depends(get_db),
):
    headers = _extract_trusted_headers(request)

    trusted_tenant_id = str(user.get("tenant_id"))
    if not trusted_tenant_id or trusted_tenant_id == "None":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant ID is missing from credentials."
        )

    headers["x-tenant-id"] = trusted_tenant_id
    auth_user_id = UUID(user["sub"])

    conv_service = ConversationService(db)
    conversation = conv_service.get_or_create_conversation(
        tenant_id=trusted_tenant_id,
        auth_user_id=auth_user_id,
        message_content=body.message,
        conversation_id=body.conversation_id
    )

    conv_service.add_message(conversation.id, "user", body.message)

    result = await coordinator.process(
        user_message=body.message,
        headers=headers,
    )

    conv_service.add_message(conversation.id, "ai", result)

    return {
        "success": True,
        "data": result,
        "conversation_id": conversation.id,
    }

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trusted_tenant_id = str(user.get("tenant_id"))
    auth_user_id = UUID(user["sub"])
    return ConversationService(db).get_conversations(trusted_tenant_id, auth_user_id)

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: UUID,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trusted_tenant_id = str(user.get("tenant_id"))
    auth_user_id = UUID(user["sub"])
    conv = ConversationService(db).get_conversation(conversation_id, trusted_tenant_id, auth_user_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: UUID,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trusted_tenant_id = str(user.get("tenant_id"))
    auth_user_id = UUID(user["sub"])
    success = ConversationService(db).delete_conversation(conversation_id, trusted_tenant_id, auth_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return Response(status_code=204)