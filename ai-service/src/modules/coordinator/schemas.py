from typing import Any, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request payload from the user.
    """
    message: str = Field(..., description="The natural language request from the user.")


class ChatResponse(BaseModel):
    """
    Standard response format returned by the Coordinator API.
    """
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
