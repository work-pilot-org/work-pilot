from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: UUID
    title: str
    date: str
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True
